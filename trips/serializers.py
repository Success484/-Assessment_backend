from rest_framework import serializers


class TripSerializer(serializers.Serializer):
    current_location = serializers.CharField()
    pickup_location = serializers.CharField()
    dropoff_location = serializers.CharField()
    current_cycle_used = serializers.FloatField(min_value=0)
