from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied 
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action 
from django.shortcuts import get_object_or_404

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
    
    @action(detail=False,methods=['get','put'],permission_classes=[IsAuthenticated])
    def me(self,request):
        print(request.user)
        doctor = get_object_or_404(Doctor,user=request.user)
        if request.method == 'GET':
            print('@@@@@@GET')
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data,status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            print('@@@@@@PUT')
            print(doctor)
            serializer = DoctorSerializer(doctor,data=request.data,context={'user':request.user})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            
    

