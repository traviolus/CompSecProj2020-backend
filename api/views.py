from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import CustomUserSerializer, CustomJWTSerializer

from users.models import CustomUser

class SignupViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        user_name = request.data['user_name']
        try:
            CustomUserSerializer.create(CustomUserSerializer(), validated_data=request.data)
        except Exception as e:
            return Response(str(e), status=400)
        return Response('User: ' + user_name + ". Registration successful!")

class SigninViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = CustomJWTSerializer

    def create(self, request, *args, **kwargs):
        try:
            token = CustomJWTSerializer.validate(CustomJWTSerializer(), attrs=request.data)
        except Exception as e:
            return Response(str(e), status=400)
        return Response(token)