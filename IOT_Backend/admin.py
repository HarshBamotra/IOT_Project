from django.contrib import admin
from .models import *


class SensorDataAdmin(admin.ModelAdmin):
    search_fields = ['node_id']
    list_display = ['node_id', 'timestamp', 'AQI', 'added_at']
    list_filter = ['node_id']

admin.site.register(SensorData, SensorDataAdmin)
