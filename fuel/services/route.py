import requests
import math
from decimal import Decimal
from fuel.models import FuelStation
from fuel.services.ai import ai_spatial_assistant

def geocode_address(address_str):
    """
    Converts a plain text location string into latitude and longitude coordinates
    using the free OpenStreetMap Nominatim API.
    """

    url = f"https://openstreetmap.org{address_str}&format=json&limit=1"
    headers = {'User-Agent': 'FuelAlgorithmicSystem/3.0'}

    try:
        response = requests.get(url, headers=headers, timeout=10).json()

        if response and len(response) > 0:
            return float(response[0]['lat']), float(response[0]['lon'])
    except Exception:
        raise ValueError(f"Geocoding network lookup failed for location: {address_str}")

    raise ValueError(f"Could not find coordinates for location entry: {address_str}")

def get_osrm_route(start_coords, finish_coords, route_type='car'):
    """
    Fetches the full driving geometry and total distance from the free OSRM API.
    Note: OSRM strictly expects coordinates in the format: longitude,latitude.
    """

    start_lat, start_lon = start_coords
    finish_lat, finish_lon = finish_coords

    if route_type not in ['car', 'bike', 'foot']:
        route_type = 'car'

    url = f"https://routing.openstreetmap.de/routed-{route_type}/route/v1/driving/{start_lon},{start_lat};{finish_lon},{finish_lat}?overview=full&geometries=geojson"

    try:
        response = requests.get(url, timeout=10).json()
    except Exception as e:
        raise Exception(f"OSRM routing network connection failed: {str(e)}")
        
    if response.get('code') != 'Ok':
        raise Exception("Failed to generate route geometry via OSRM map servers.")
        
    route = response['routes'][0]
    distance_miles = route['distance'] * 0.000621371
    route_geometry = route['geometry']

    return distance_miles, route_geometry

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the straight-line distance in miles between two coordinate points
    across the Earth's curvature.
    """

    if None in (lat1, lon1, lat2, lon2):
        return float('inf')

    R = 3958.8
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2

    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def optimize_fuel_route(route_geometry, total_distance):
    """
    Calculates mathematically optimal cost-effective fuel stops along the route.
    Constraints: 500-mile max vehicle tank range, 10 Miles Per Gallon efficiency.
    Optimized with cumulative path metrics and fast spatial indexing arrays.
    """

    coordinates = route_geometry['coordinates']

    route_milemarkers = [0.0]
    cumulative_dist = 0.0

    for i in range(len(coordinates) - 1):
        p1 = coordinates[i]
        p2 = coordinates[i+1]
        cumulative_dist += haversine_distance(p1[1], p1[0], p2[1], p2[0])
        route_milemarkers.append(cumulative_dist)

    ai_spatial_assistant.train_clusters()
    candidate_stations = ai_spatial_assistant.get_intersecting_stations(coordinates)

    sample_step = max(1, len(coordinates) // 100)
    sampled_indices = list(range(0, len(coordinates), sample_step))
    if sampled_indices[-1] != len(coordinates) - 1:
        sampled_indices.append(len(coordinates) - 1)

    stations_with_markers = []
    for station in candidate_stations:
        min_dist = float('inf')
        closest_idx = 0

        for idx in sampled_indices:
            lon, lat = coordinates[idx]
            d = haversine_distance(lat, lon, station['latitude'], station['longitude'])

            if d < min_dist:
                min_dist = d
                closest_idx = idx
                
        milemarker = route_milemarkers[closest_idx]
        
        stations_with_markers.append({
            'station': station,
            'milemarker': milemarker
        })
        
    stations_with_markers.sort(key=lambda x: x['milemarker'])

    max_range = 500.0
    mpg = 10.0
    current_mile = 0.0
    total_cost = Decimal('0.00')
    selected_stops = []
    
    stations_with_markers.append({'station': None, 'milemarker': total_distance})
    
    i = 0
    num_elements = len(stations_with_markers)
    
    while current_mile < total_distance:
        reachable = []
        for j in range(i, num_elements):
            dist_to_node = stations_with_markers[j]['milemarker'] - current_mile
            if 0 < dist_to_node <= max_range:
                reachable.append((j, stations_with_markers[j]))
            elif dist_to_node > max_range:
                break
                
        if not reachable:
            raise ValueError("The distance gap between available corridor fuel stations exceeds the 500-mile vehicle range.")
            
        if reachable[-1]['station'] is None:
            if not selected_stops:
                miles_driven = total_distance - current_mile
                gallons_consumed = Decimal(str(miles_driven / mpg))
                total_cost = gallons_consumed * Decimal('3.50')
            break
            
        best_idx, best_node = min(
            reachable, 
            key=lambda x: x['station']['retail_price'] if x['station'] else Decimal('999.99')
        )
        station_obj = best_node['station']
        miles_driven = best_node['milemarker'] - current_mile
        
        gallons_consumed = Decimal(str(miles_driven / mpg))
        cost = gallons_consumed * station_obj['retail_price']
        
        total_cost += cost
        
        selected_stops.append({
            'opis_id': station_obj['opis_id'],
            'name': station_obj['name'],
            'address': f"{station_obj['address']}, {station_obj['city']}, {station_obj['state']}",
            'retail_price': float(station_obj['retail_price']),
            'mile_marker': round(best_node['milemarker'], 2),
            'latitude': station_obj['latitude'],
            'longitude': station_obj['longitude']
        })
        
        current_mile = best_node['milemarker']
        i = best_idx + 1

    return selected_stops, round(float(total_cost), 2)
