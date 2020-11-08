from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import CustomUserSerializer, CustomJWTSerializer, TopicSerializer, CommentSerializer

from users.models import CustomUser
from topics.models import Topic
from comments.models import Comment

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
            return Response('Bad user token', status=401)
            
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

    def partial_update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response('Bad user token', status=401)
        if not request.data:
            return Response('Empty request body', status=400)

        topic_id = self.kwargs['pk']
        try:
            topic = Topic.objects.get(topic_id=topic_id)
        except Topic.DoesNotExist:
            return Response('The given topic id is not found', status=404)
        except Exception as e:
            return Response(data=str(e), status=400)

        if request.user.user_name != topic.topic_user.user_name:
            return Response('This user is not the owner of this topic', status=401)
        
        try:
            TopicSerializer.update(self, topic, validated_data=request.data)
            return Response('Edited topic successfully', status=200)
        except Exception as e:
            raise e
            return Response(data=str(e), status=400)

class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = CommentSerializer

    def get_queryset(self):
        topic = self.request.query_params.get('topic')
        if topic is not None :
            queryset = Comment.objects.filter(comment_topic__topic_id=topic)
        else : queryset = Comment.objects.all()
        return queryset.order_by('comment_createdtime')

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response('Bad user token', status=401)
        
        try:
            serializer = self.get_serializer(data={
                'comment_user': request.user.user_name,
                'comment_text': request.data['comment'],
                'comment_topic': request.data['topic_id']
            })
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response('Created Comment Successfully', status=200)
        except Exception as e:
            return Response(data=str(e), status=400)