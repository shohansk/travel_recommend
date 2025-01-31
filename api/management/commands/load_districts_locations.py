import json
from django.core.management.base import BaseCommand
from api.models import DistrictsLocations


class Command(BaseCommand):
    help = "Load districts from a JSON file into the database"

    def handle(self, *args, **kwargs):
        with open("data/dynamic/districts.json", "r") as file:
            districts_data = json.load(file)

        for district in districts_data["districts"]:
            location, created = DistrictsLocations.objects.update_or_create(
                id=district["id"],
                defaults={
                    "division_id": district["division_id"],
                    "name": district["name"],
                    "bn_name": district["bn_name"],
                    "lat": district["lat"],
                    "long": district["long"],
                },
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
