from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Doctor,Patient
from .serializers import DoctorSerializer

class DoctorViewSet(ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_context(self):
        return {'user':self.request.user}




