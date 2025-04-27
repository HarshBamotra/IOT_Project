from django.db import models

class SensorData(models.Model):
    node_id = models.CharField(max_length=256)
    timestamp = models.DateTimeField()
    pm2_5 = models.FloatField(default=0.0)
    pm10 = models.FloatField(default=0.0)
    NO = models.FloatField(default=0.0)
    NO2 = models.FloatField(default=0.0)
    NOX = models.FloatField(default=0.0)
    NH3 = models.FloatField(default=0.0)
    CO = models.FloatField(default=0.0)
    SO2 = models.FloatField(default=0.0)
    O3 = models.FloatField(default=0.0)
    Benzene = models.FloatField(default=0.0)
    Toluene = models.FloatField(default=0.0)
    Xylene = models.FloatField(default=0.0)
    AQI = models.FloatField(default=0.0)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['node_id', 'timestamp'], name='node_id'),
        ]