from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *


@api_view(['GET', 'POST'])
def getMoteData(request):
    try:
        if request.method == 'GET':
            node_id = request.GET.get('node_id')

            if node_id:
                sensorData = SensorData.objects.filter(node_id=node_id)
            else:
                sensorData = SensorData.objects.all()

            if sensorData:
                sensorData = SensorDataSerializers(sensorData, many=True)
                return Response({'message': 'Success', "sensorData": sensorData.data}, status=status.HTTP_200_OK)
            return Response({"message": f"No data present for sensor."}, status=status.HTTP_200_OK)
        
        elif request.method == 'POST':
            data = request.data
            if data:
                if isinstance(data, list):
                    sensor_data = []
                    for sensor in data:
                        sensor_data.append(SensorData(**sensor))
                    SensorData.objects.bulk_create(sensor_data)
                elif isinstance(data, dict):
                    SensorData.objects.create(**data)
                else:
                    return Response({'message': 'Invalid Format or incorrect data.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Please post data to process.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Success'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': f'Error Occured: {e}'}, status=status.HTTP_400_BAD_REQUEST)
