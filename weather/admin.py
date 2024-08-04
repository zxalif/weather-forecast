from django.contrib import admin

from .models import District, WeatherData

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'longitude',
        'latitude'
    ]
    search_fields = ['name']


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    fields = [
        'district',
        'date',
        'time',
        'temperature'
    ]
    raw_id_fields = ['district']
