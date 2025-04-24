from django.contrib import admin
from .models import *


class SensorDataAdmin(admin.ModelAdmin):
    search_fields = ['mote_id']
    list_display = ['mote_id', 'timestamp', 'location', 'temperature', 'gas_concentration']
    list_filter = ['mote_id']

admin.site.register(SensorData, SensorDataAdmin)
