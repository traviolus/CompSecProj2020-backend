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
        return Response('User: ' + user_name + ". Registration successful!", status=200)

class SigninViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = CustomJWTSerializer

    def create(self, request, *args, **kwargs):
        try:
            token = CustomJWTSerializer.validate(CustomJWTSerializer(), attrs=request.data)
        except Exception as e:
            return Response(str(e), status=400)
        return Response(token, status=200)

class TopicViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = CustomUser.objects.get(user_id=request.user.user_id)
        else:
            return Response('The user is not authenticated.', status=401)
            
        #Create Topic Object
        try:
            serializer = self.get_serializer(data={
                'topic_header': request.data['topic_header'],
                'topic_body': request.data['topic_body'],
                'topic_user': request.user.user_name,
            })
            
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(data="Created Topic Successfully.", status=200)
        except Exception as e:
            return Response(data=str(e), status=400)