from rest_framework import serializers
from api.models import DistrictsLocations

class DistrictsLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistrictsLocations
        fields = ['id', 'name', 'bn_name', 'lat', 'long']
