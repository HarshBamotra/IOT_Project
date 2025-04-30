from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import csv
import io
import os

from .models import *
from .serializers import *


CSV_FILE = 'sensor_data.csv'
FIELDNAMES = [
    "id", "node_id", "timestamp",
    "pm2_5", "pm10", "NO", "NO2", "NOX", "NH3",
    "CO", "SO2", "O3", "Benzene", "Toluene", "Xylene",
    "AQI", "added_at"
]

def create_base_entry(idx: int):
    now = datetime.utcnow().isoformat() + "Z"
    return {
        "id": idx,
        "node_id": str(idx),
        "timestamp": now,
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
        "added_at": now
    }

def write_csv(data: list[dict]):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(data)

def load_csv() -> list[dict]:
    if not os.path.exists(CSV_FILE):
        # bootstrap with 50 entries
        data = [create_base_entry(i) for i in range(1, 51)]
        write_csv(data)
        return data

    data = []
    with open(CSV_FILE, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # convert types
            sensor = {
                "id": int(row["id"]),
                "node_id": row["node_id"],
                "timestamp": row["timestamp"],
                "pm2_5": float(row["pm2_5"]),
                "pm10": float(row["pm10"]),
                "NO": float(row["NO"]),
                "NO2": float(row["NO2"]),
                "NOX": float(row["NOX"]),
                "NH3": float(row["NH3"]),
                "CO": float(row["CO"]),
                "SO2": float(row["SO2"]),
                "O3": float(row["O3"]),
                "Benzene": float(row["Benzene"]),
                "Toluene": float(row["Toluene"]),
                "Xylene": float(row["Xylene"]),
                "AQI": float(row["AQI"]),
                "added_at": row["added_at"]
            }
            data.append(sensor)
    return data

# Global in‐memory cache (always kept in sync with disk)
current_sensor_data = load_csv()
    

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
                    
            write_csv(current_sensor_data)
            return Response({'message': f'CSV processed, updated {updated} sensors.'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'message': f'Error Occurred: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
