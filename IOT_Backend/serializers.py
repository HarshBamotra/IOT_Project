from rest_framework import serializers
from .models import SensorData

class SensorDataSerializers(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = '__all__'