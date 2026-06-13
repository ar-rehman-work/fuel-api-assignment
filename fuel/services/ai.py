import numpy as np
from sklearn.cluster import KMeans
from fuel.models import FuelStation

class SpatialFuelClusterer:
    """An AI-driven Unsupervised Learning service that clusters US fuel 
    stations into high-density regional hubs to optimize spatial route queries.
    """

    def __init__(self, n_clusters=50):
        self.n_clusters = n_clusters
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=42, n_init='auto')
        self.is_trained = False

    def train_clusters(self):
        """
        Trains the K-Means AI model on all station coordinates in the database.
        """
        coordinates_list = FuelStation.objects.values_list('latitude', 'longitude')
        
        if not coordinates_list.exists():
            return

        coordinates_matrix = np.array(list(coordinates_list))
        
        if len(coordinates_matrix) >= self.n_clusters:
            self.kmeans.fit(coordinates_matrix)
            self.is_trained = True

    def get_intersecting_stations(self, route_coordinates):
        """
        AI Inference: Predicts which fueling hub clusters intersect the route path,
        filtering down candidate stations with high algorithmic efficiency.
        """
        if not self.is_trained:
            return list(FuelStation.objects.values(
                'id', 'opis_id', 'name', 'address', 'city', 'state', 'retail_price', 'latitude', 'longitude'
            ))

        route_points = np.array([[pt[1], pt[0]] for pt in route_coordinates])
        
        predicted_route_clusters = self.kmeans.predict(route_points)
        unique_intersecting_clusters = set(predicted_route_clusters)

        station_data = list(FuelStation.objects.values(
            'id', 'opis_id', 'name', 'address', 'city', 'state', 'retail_price', 'latitude', 'longitude'
        ))

        if not station_data:
            return []

        station_coords_matrix = np.array([[item['latitude'], item['longitude']] for item in station_data])
        all_station_predicted_clusters = self.kmeans.predict(station_coords_matrix)

        matching_stations = []
        for idx, cluster_id in enumerate(all_station_predicted_clusters):
            if cluster_id in unique_intersecting_clusters:
                matching_stations.append(station_data[idx])

        return matching_stations

# Singleton Object
ai_spatial_assistant = SpatialFuelClusterer(n_clusters=50)
