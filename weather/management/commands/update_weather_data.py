import requests
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from weather.models import District, WeatherData


class Command(BaseCommand):
    help = 'Fetch and update weather data for all districts'

    def handle(self, *args, **kwargs):
        one_hour_ago = timezone.now() - timedelta(hours=1)
        districts = District.objects.filter(last_updated__lt=one_hour_ago)
        for district in districts:
            self.fetch_and_store_weather_data(district)

        self.stdout.write(self.style.SUCCESS(f'Updated weather.'))

    def fetch_and_store_weather_data(self, district):
        url = f"https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': district.latitude,
            'longitude': district.longitude,
            'hourly': 'temperature_2m',
            'start': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'end': (datetime.utcnow() + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'timezone': 'Asia/Dhaka',
            'temperature_unit': 'celsius'  # Or 'fahrenheit' if needed
        }
        response = requests.get(url, params=params)
        weather_data = response.json()
        hourly_data = weather_data.get('hourly', {}).get('temperature_2m', [])
        timestamps = weather_data.get('hourly', {}).get('time', [])

        for i, temp in enumerate(hourly_data):
            timestamp = timestamps[i]
            date, time = timestamp.split('T')
            time = time[:5]  # Extract HH:MM

            WeatherData.objects.update_or_create(
                district=district,
                date=date,
                time=time,
                defaults={'temperature': temp, 'last_updated': datetime.now()}
            )
        self.stdout.write(self.style.SUCCESS(f'Updated weather data for {district.name}'))
