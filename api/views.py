from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import CustomUserSerializer, CustomJWTSerializer, TopicSerializer

from users.models import CustomUser
from topics.models import Topic

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

class TopicViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = TopicSerializer

    def get_queryset(self):
        tag = self.request.query_params.get('tag')
        if tag is not None :
            queryset = Topic.objects.filter(topic_tag__tag_name=tag)
        else : queryset = Topic.objects.all()
        return queryset