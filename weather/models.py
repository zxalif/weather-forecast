from django.db import models


class District(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class WeatherData(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    temperature = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        formatted_date = self.date.strftime('%b %d, %Y')
        formatted_time = self.time.strftime('%I:%M %p')
        return f'{self.district.name} on {formatted_date} at {formatted_time}'

    class Meta:
        unique_together = ('district', 'date', 'time')
