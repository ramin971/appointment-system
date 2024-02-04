from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.exceptions import PermissionDenied ,NotAcceptable
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action,api_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404

from .permissions import IsOwnerOrReadOnly,AuthenticateOrWriteOnly
from .models import Doctor,Patient,MeetingTime
from .serializers import DoctorSerializer,CreateDoctorSerializer,PatientSerializer,MeetingTimeSerializer,BulkCreateMeetingTimeSerializer

class DoctorViewSet(ModelViewSet):
    queryset = Doctor.objects.select_related('user').all()
    # serializer_class = DoctorSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateDoctorSerializer
        return DoctorSerializer

    def get_serializer_context(self):
        return {'user':self.request.user}
    
    @action(detail=False,methods=['get','put','delete'],permission_classes=[IsAuthenticated])# permission_classes = [IsDoctor] # if this ==> get_ser_cont:doctor=d.ob.filter
    def me(self,request):
        doctor = get_object_or_404(Doctor,user=request.user) # converte to get
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
        elif request.method == 'DELETE':
            doctor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
           
    
class PatientViewSet(ListCreateAPIView):
    # queryset = Patient.objects.select_related('time','doctor__user').filter('doctor'=self.request.user)
    filter_backends = [DjangoFilterBackend,SearchFilter]
    # filterset_fields = ['doctor', 'date']
    filterset_fields = {
      'date':[ 'gte', 'lte'],
      'doctor':['exact']}
    search_fields = ['fullname','national_code']
    pagination_class = PageNumberPagination
    permission_classes = [AuthenticateOrWriteOnly]
    serializer_class = PatientSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            # print('###################',self.request.user.is_superuser,self.request.user.is_staff)
            return Patient.objects.select_related('time','doctor__user').all()
        return Patient.objects.select_related('time','doctor__user').filter(doctor=self.request.user.id)

class MeetingTimeViewSet(ModelViewSet):
    # queryset = MeetingTime.objects.all()
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsDoctor] # if this ==> get_ser_cont:doctor=d.ob.filter
    serializer_class = MeetingTimeSerializer

    def get_queryset(self):
        return MeetingTime.objects.select_related('doctor__user').filter(doctor=self.request.user.id)

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data,many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_serializer_context(self):
        doctor=get_object_or_404(Doctor,user=self.request.user)
        # doctor = Doctor.objects.filter(user=self.request.user)
        return {'doctor':doctor}

        
    
@api_view(['GET'])
def relatedtime(request,pk):
    queryset = MeetingTime.objects.filter(doctor=pk)
    serializer = MeetingTimeSerializer(queryset,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)