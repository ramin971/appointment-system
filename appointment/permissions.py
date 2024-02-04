from rest_framework import permissions
from .models import Doctor

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        elif request.method == 'POST':
            return bool(request.user and request.user.is_staff)
        else:
            return bool(
                (str(request.user.id) == view.kwargs.get('pk')) and
                request.user.is_authenticated
                
            )

class AuthenticateOrWriteOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(True)
    
    #  and (Doctor.objects.filter(user=request.user).exists())