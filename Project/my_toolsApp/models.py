from django.db import models

# Create your models here.
class NewsWeather(models.Model):
    ip = models.CharField(primary_key=True, max_length=255)
    weather_info = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news_weather'


