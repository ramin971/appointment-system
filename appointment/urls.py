from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'doctor', views.DoctorViewSet)
urlpatterns = [
    path('',include(router.urls)),
]
