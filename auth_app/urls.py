from django.urls import path,include
from . import views

urlpatterns = [
    path('',include('djoser.urls')),
    path('jwt/create/',views.CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/',views.CustomTokenRefreshView.as_view())

]
