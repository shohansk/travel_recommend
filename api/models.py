from django.db import models


class DistrictsLocations(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.AutoField(primary_key=True)
    division_id = models.IntegerField()
    name = models.CharField(max_length=255)
    bn_name = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=10, decimal_places=8)
    long = models.DecimalField(max_digits=10, decimal_places=8)

    class Meta:
        db_table = "districts_locations"
