from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone

from users.models import CustomUser
from topics.models import Topic
from comments.models import Comment

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            user_name=validated_data.pop("user_name"),
            password=validated_data.pop("password"),
            user_email=validated_data.pop("user_email"),
        )
        user.save()
        return user

class CustomJWTSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        credentials = {
            "user_name": attrs.get("user_name"),
            "password": attrs.get("password"),
        }
        user_obj = (
            CustomUser.objects.filter(user_name=attrs.get("user_name")).first() or
            CustomUser.objects.filter(user_email=attrs.get("user_name")).first()
        )
        if user_obj:
            credentials["user_name"] = user_obj.user_name
        return super().validate(credentials), {'user_name': credentials['user_name']}

class TopicSerializer(serializers.ModelSerializer):
    topic_user = serializers.CharField(source='get_user_name')

    class Meta:
        model = Topic
        fields = "__all__"

    def create(self, validated_data):
        new_topic = Topic.objects.create(
            topic_header=validated_data.pop('topic_header'),
            topic_body=validated_data.pop('topic_body'),
            topic_user=CustomUser.objects.get(user_name=validated_data.pop('get_user_name'))
        )
        new_topic.save()
        return new_topic

    def update(self, instance, validated_data):
        if 'topic_header' in validated_data: 
            instance.topic_header = validated_data.pop('topic_header')
        if 'topic_body' in validated_data:
            instance.topic_body = validated_data.pop('topic_body')
        instance.topic_lastmodified = timezone.now()
        instance.save()
            
class CommentSerializer(serializers.ModelSerializer):
    comment_user = serializers.CharField(source='get_user_name')

    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        new_comment = Comment.objects.create(
            comment_text=validated_data.pop('comment_text'),
            comment_user=CustomUser.objects.get(user_name=validated_data.pop('get_user_name')),
            comment_topic=validated_data.pop('comment_topic')
        )
        new_comment.save()
        return new_comment