from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *


@api_view(['GET'])
def getMoteData(request):
    try:
        mote_id = request.GET.get('mote_id')

        if mote_id:
            sensorData = SensorData.objects.filter(mote_id=mote_id)
        else:
            sensorData = SensorData.objects.all()

        if sensorData:
            sensorData = SensorDataSerializers(sensorData, many=True)
            return Response({'message': 'Success', "sensorData": sensorData.data}, status=status.HTTP_200_OK)
        return Response({"message": f"No data present for sensor."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': f'Error Occured: {e}'}, status=status.HTTP_400_BAD_REQUEST)
