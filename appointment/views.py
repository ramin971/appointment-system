from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied 
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .permissions import IsOwnerOrReadOnly
from .models import Doctor,Patient
from .serializers import DoctorSerializer,CreateDoctorSerializer

class DoctorViewSet(ModelViewSet):
    queryset = Doctor.objects.all()
    # serializer_class = DoctorSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateDoctorSerializer
        return DoctorSerializer

    def get_serializer_context(self):
        return {'user':self.request.user}

    
    

