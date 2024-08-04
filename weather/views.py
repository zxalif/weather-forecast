from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from weather.models import District, WeatherData

class CoolestDistrictsView(APIView):
    def get(self, request):
        today = timezone.now().date()
        seven_days_later = today + timedelta(days=7)
        districts_avg_temp = WeatherData.objects.filter(
            date__gte=today,
            date__lte=seven_days_later,
            time='14:00:00'
        ).values('district').annotate(
            avg_temp=Avg('temperature')
        ).order_by('avg_temp')[:10]

        coolest_districts = []
        for data in districts_avg_temp:
            district = District.objects.get(id=data['district'])
            coolest_districts.append({
                'name': district.name,
                'avg_temp': data['avg_temp']
            })

        return Response(coolest_districts, status=status.HTTP_200_OK)


class TravelAdviceView(APIView):
    def get(self, request, from_district, to_district, travel_date):
        from_location = get_object_or_404(District, id=from_district)
        destination = get_object_or_404(District, id=to_district)

        try:
            from_temp = WeatherData.objects.get(
                district=from_location,
                date=travel_date,
                time='14:00:00'
            )

            destination_temp = WeatherData.objects.get(
                district=destination,
                date=travel_date,
                time='14:00:00'
            )
        except WeatherData.DoesNotExist:
            return Response({'error': 'Weather data not available for the given date'}, status=status.HTTP_404_NOT_FOUND)

        advice = 'Cold not generate any better advice'
        if destination_temp.temperature > from_temp.temperature:
            advice = 'Destination weather is hot'
        elif destination_temp.temperature < from_temp.temperature:
            advice = 'Home weather is Hot, safe to visit!'
        elif destination_temp.temperature == from_temp.temperature:
            advice = 'Same temperature, wouldn\'t hurt to travel!'

        resp = {
            'from': from_location.name,
            'from_temp': from_temp.temperature,
            'destination': destination.name,
            'destination_temp': destination_temp.temperature,
            'advice': advice
        }
        if from_district == to_district:
            resp['warning'] = 'For your FYI, trying to visit same district'
        return Response(resp, status=status.HTTP_200_OK)

