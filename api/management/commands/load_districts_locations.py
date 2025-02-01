from django.core.management.base import BaseCommand
from api.serializers import DistrictsLocationsSerializer
from api.models import DistrictsLocations
import json


class Command(BaseCommand):
    help = "Load districts from a JSON file into the database"

    def handle(self, *args, **kwargs):
        with open("data/dynamic/districts.json", "r") as file:
            districts_data = json.load(file)
        for district in districts_data["districts"]:
            serializer = DistrictsLocationsSerializer(data=district)
            if serializer.is_valid():
                instance, created = DistrictsLocations.objects.update_or_create(
                    id=district["id"],
                    defaults=serializer.validated_data,
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"District '{district['name']}' created successfully"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"District '{district['name']}' updated successfully"
                        )
                    )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f"Validation error for district '{district['name']}': {serializer.errors}"
                    )
                )
