from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=False, allow_blank=True, default='')
    password = serializers.CharField(required=True, write_only=True, min_length=8)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )

class RouteInputSerializer(serializers.Serializer):
    start = serializers.CharField(
        required=True, 
        max_length=255, 
        help_text="Starting location in US (e.g., 'New York, NY' or '123 Main St, Chicago, IL')."
    )
    finish = serializers.CharField(
        required=True, 
        max_length=255, 
        help_text="Final location in US (e.g., 'Los Angeles, CA' or '456 Broadway, Miami, FL')."
    )
    route_type = serializers.ChoiceField(
        choices=[
            ('car', 'Car'), 
            ('bike', 'Bike'), 
            ('foot', 'Pedestrian')
        ], 
        default='car', 
        required=False,
        help_text="Mode of transit selection menu option."
    )

class RouteSummarySerializer(serializers.Serializer):
    start = serializers.CharField()
    finish = serializers.CharField()
    total_distance_miles = serializers.FloatField()
    total_fuel_cost_usd = serializers.FloatField()
    fuel_efficiency = serializers.CharField(default="10 MPG")
    max_tank_range = serializers.CharField(default="500 miles")

class OptimalFuelStopSerializer(serializers.Serializer):
    opis_id = serializers.IntegerField()
    name = serializers.CharField()
    address = serializers.CharField()
    retail_price = serializers.FloatField()
    mile_marker = serializers.FloatField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

class GeoJSONFeatureSerializer(serializers.Serializer):
    type = serializers.CharField(default="Feature")
    properties = serializers.JSONField()
    geometry = serializers.JSONField()

class GeoJSONCollectionSerializer(serializers.Serializer):
    type = serializers.CharField(default="FeatureCollection")
    features = GeoJSONFeatureSerializer(many=True)

class RouteOptimizerResponseSerializer(serializers.Serializer):
    summary = RouteSummarySerializer()
    optimal_fuel_stops = OptimalFuelStopSerializer(many=True)
    map_route_data = GeoJSONCollectionSerializer()
