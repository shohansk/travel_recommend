from rest_framework import serializers
from .models import DistrictsLocations


class DistrictsLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistrictsLocations
        fields = ["id", "division_id", "name", "bn_name", "lat", "long"]
