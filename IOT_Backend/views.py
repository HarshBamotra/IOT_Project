from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import csv
import io

from .models import *
from .serializers import *


# Base single sensor template
def create_base_entry():
    return {
        "id": 0,
        "node_id": "0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "pm2_5": 175.0541244,
        "pm10": 225.6159204,
        "NO": 63.16595663,
        "NO2": 81.20394571,
        "NOX": 22.26520486,
        "NH3": 38.14978342,
        "CO": 18.55,
        "SO2": 54.37004314,
        "O3": 2.033851062,
        "Benzene": 1.29022789,
        "Toluene": 2.545848505,
        "Xylene": 5.436573227,
        "AQI": 0,
        "added_at": datetime.utcnow().isoformat() + "Z"
    }

# Initialize global sensor data store
current_sensor_data = [create_base_entry() for _ in range(50)]
for idx, sensor in enumerate(current_sensor_data, start=1):
    sensor["id"] = idx
    sensor["node_id"] = str(idx)
    

@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser])
def getMoteData(request):
    try:
        if request.method == 'GET':
            return Response({'message': 'Success', "sensorData": current_sensor_data}, status=status.HTTP_200_OK)
        
        elif request.method == 'POST':
            if 'file' not in request.FILES:
                return Response({'message': 'Please post data to process.'}, status=status.HTTP_400_BAD_REQUEST)
            
            file = request.FILES['file']
            content = file.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(content))

            # Map CSV headers to sensor keys
            header_map = {
                'Timestamp': 'timestamp',
                'Node ID': 'node_id',
                'PM2.5': 'pm2_5',
                'PM10': 'pm10',
                'NO': 'NO',
                'NO2': 'NO2',
                'NOx': 'NOX',
                'NH3': 'NH3',
                'CO': 'CO',
                'SO2': 'SO2',
                'O3': 'O3',
                'Benzene': 'Benzene',
                'Toluene': 'Toluene',
                'Xylene': 'Xylene',
                'AQI': 'AQI'
            }

            updated = 0
            for row in reader:
                node = row.get('Node ID', '').strip()
                if not node:
                    continue
                for sensor in current_sensor_data:
                    if sensor['node_id'] == node:
                        for csv_key, value in row.items():
                            sensor_key = header_map.get(csv_key)
                            if not sensor_key or sensor_key in ('id', 'node_id'):
                                continue
                            if sensor_key == 'timestamp':
                                sensor['timestamp'] = value
                            else:
                                try:
                                    sensor[sensor_key] = float(value)
                                except:
                                    pass
                        sensor['added_at'] = datetime.utcnow().isoformat() + 'Z'
                        updated += 1
                        break

            return Response({'message': f'CSV processed, updated {updated} sensors.'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'message': f'Error Occurred: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
