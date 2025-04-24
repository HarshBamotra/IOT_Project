from django.db import models

class SensorData(models.Model):
    mote_id = models.CharField(max_length=256)
    timestamp = models.DateTimeField()
    location = models.CharField(max_length=256)
    temperature = models.FloatField(default=0.0)
    gas_concentration = models.FloatField(default=0.0)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['mote_id', 'timestamp'], name='mote_id'),
        ]