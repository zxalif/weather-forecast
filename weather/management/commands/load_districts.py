import json
from django.core.management.base import BaseCommand
from weather.models import District
import requests

class Command(BaseCommand):
    help = 'Load district data from JSON file'

    def handle(self, *args, **kwargs):
        response = requests.get("https://raw.githubusercontent.com/strativ-dev/technical-screening-test/main/bd-districts.json")
        for district in response.json().get("districts", []):
            # create the district, asuming the name is unique
            District.objects.get_or_create(
                name=district['name'],
                latitude=district['lat'],
                longitude=district['long']
            )
        self.stdout.write(self.style.SUCCESS('District data loaded successfully'))
