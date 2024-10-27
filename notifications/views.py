#notifications/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Device

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_device_token(request):
    token = request.data.get('device_token')
    if token:
        device, created = Device.objects.get_or_create(
            user=request.user,
            device_token=token  # Use the correct field name here
        )
        if created:
            return Response({'status': 'success', 'message': 'Device token registered.'}, status=201)
        else:
            return Response({'status': 'success', 'message': 'Device token already exists.'}, status=200)
    else:
        return Response({'error': 'No token provided'}, status=400)