from rest_framework_simplejwt.serializers import TokenRefreshSerializer as BaseTokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken,TokenError
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','username','password','first_name','last_name']



class TokenRefreshSerializer(BaseTokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        raise InvalidToken
