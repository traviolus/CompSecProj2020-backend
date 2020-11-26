from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import CustomUserSerializer, CustomJWTSerializer, TopicSerializer, CommentSerializer

from users.models import CustomUser
from topics.models import Topic
from comments.models import Comment

custom_headers = {"Content-Security-Policy" : "frame-ancestors 'none'", "X-Frame-Options" : "DENY"}

class SignupViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        user_name = request.data['user_name']
        try:
            CustomUserSerializer.create(CustomUserSerializer(), validated_data=request.data)
        except Exception as e:
            return Response(str(e), status=400, headers=custom_headers)
        return Response('User: ' + user_name + ". Registration successful!", status=200, headers=custom_headers)

class SigninViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = CustomJWTSerializer

    def create(self, request, *args, **kwargs):
        try:
            token, user = CustomJWTSerializer.validate(CustomJWTSerializer(), attrs=request.data)
        except Exception as e:
            return Response(str(e), status=400, headers=custom_headers)
        return Response(data=dict(user, **token), status=200, headers=custom_headers)

class TopicViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = CustomUser.objects.get(user_id=request.user.user_id)
        else:
            return Response('Bad user token', status=401, headers=custom_headers)
            
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
            return Response(data="Created Topic Successfully.", status=200, headers=custom_headers)
        except Exception as e:
            return Response(data=str(e), status=400, headers=custom_headers)

    def partial_update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response('Bad user token', status=401, headers=custom_headers)
        if not request.data:
            return Response('Empty request body', status=400, headers=custom_headers)

        topic_id = self.kwargs['pk']
        try:
            topic = Topic.objects.get(topic_id=topic_id)
        except Topic.DoesNotExist:
            return Response('The given topic id is not found', status=404, headers=custom_headers)
        except Exception as e:
            return Response(data=str(e), status=400, headers=custom_headers)

        if request.user.user_name != topic.topic_user.user_name and request.user.get_user_status_display() != 'admin':
            return Response('This user is not the owner of this topic', status=401, headers=custom_headers)
        
        try:
            TopicSerializer.update(self, topic, validated_data=request.data)
            return Response('Edited topic successfully', status=200, headers=custom_headers)
        except Exception as e:
            return Response(data=str(e), status=400, headers=custom_headers)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response('Bad user token', status=401, headers=custom_headers)
        if request.user.get_user_status_display() != 'admin':
            return Response('You do not have permission to delete.', status=403, headers=custom_headers)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response("Deleted.", status=200, headers=custom_headers)

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
            return Response('Bad user token', status=401, headers=custom_headers)
        
        try:
            serializer = self.get_serializer(data={
                'comment_user': request.user.user_name,
                'comment_text': request.data['comment'],
                'comment_topic': request.data['topic_id']
            })
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response('Created Comment Successfully', status=200, headers=custom_headers)
        except Exception as e:
            return Response(data=str(e), status=400, headers=custom_headers)

    def partial_update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response('Bad user token', status=401, headers=custom_headers)
        if not request.data:
            return Response('Empty request body', status=400, headers=custom_headers)

        comment_id = self.kwargs['pk']
        try:
            comment = Comment.objects.get(comment_id=comment_id)
        except Comment.DoesNotExist:
            return Response('The given comment id is not found', status=404, headers=custom_headers)
        except Exception as e:
            return Response(data=str(e), status=400, headers=custom_headers)

        if request.user.user_name != comment.comment_user.user_name and request.user.get_user_status_display() != 'admin':
            return Response('This user is not the owner of this topic', status=401, headers=custom_headers)
        
        try:
            CommentSerializer.update(self, comment, validated_data=request.data)
            return Response('Edited comment successfully', status=200, headers=custom_headers)
        except Exception as e:
            return Response(data=str(e), status=400, headers=custom_headers)