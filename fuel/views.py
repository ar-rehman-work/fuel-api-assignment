from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from fuel.serializers import RegisterSerializer, RouteInputSerializer, RouteOptimizerResponseSerializer
from fuel.services.route import geocode_address, get_osrm_route, optimize_fuel_route

class RegisterView(APIView):
    """
    Public POST endpoint to create a new user account.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()

        return Response({"message": "User created successfully.", "username": user.username}, status=status.HTTP_201_CREATED)

class FuelRouteOptimizerView(APIView):
    """
    Secured POST API Endpoint that calculates the most cost effective fueling stops
    along a USA route using OSRM mapping and K-Means AI spatial geofencing.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        input_serializer = RouteInputSerializer(data=request.data)

        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        start_location = input_serializer.validated_data['start']
        finish_location = input_serializer.validated_data['finish']
        route_type = input_serializer.validated_data.get('route_type', 'car')
        
        try:
            start_coords = geocode_address(start_location)
            finish_coords = geocode_address(finish_location)
            total_distance, route_geometry = get_osrm_route(start_coords, finish_coords, route_type)
            optimal_stops, total_fuel_cost = optimize_fuel_route(route_geometry, total_distance)
            
            raw_response_data = {
                "summary": {
                    "start": start_location,
                    "finish": finish_location,
                    "start_coords": start_coords,
                    "finish_coords": finish_coords,
                    "total_distance_miles": round(total_distance, 2),
                    "total_fuel_cost_usd": total_fuel_cost,
                },
                "optimal_fuel_stops": optimal_stops,
                "map_route_data": {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "properties": {
                                "type": "route_line",
                                "distance_miles": round(total_distance, 2)
                            },
                            "geometry": route_geometry
                        }
                    ]
                }
            }
            
            response_serializer = RouteOptimizerResponseSerializer(data=raw_response_data)
            response_serializer.is_valid(raise_exception=True)
            
            return Response(response_serializer.data, status=status.HTTP_200_OK)
            
        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            return Response({"error": f"Internal Routing Failure: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
