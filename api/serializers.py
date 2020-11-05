from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import CustomUser
from topics.models import Topic
from tags.models import Tag

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
        return super().validate(credentials)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag_name',)

class TopicSerializer(serializers.ModelSerializer):
    topic_tag = serializers.ListField(source='get_tag_name')
    topic_user = serializers.CharField(source='get_user_name')

    class Meta:
        model = Topic
        fields = "__all__"

    def create(self, validated_data):
        tag_list = []
        for tag_data in validated_data.pop('get_tag_name'):
            try:
                tag_instance = Tag.objects.get(tag_name=tag_data)
            except:
                tag_instance = Tag.objects.create(tag_name=tag_data)
            tag_list.append(tag_instance)
        
        new_topic = Topic.objects.create(
            topic_header=validated_data.pop('topic_header'),
            topic_body=validated_data.pop('topic_body'),
            topic_user=CustomUser.objects.get(user_name=validated_data.pop('get_user_name'))
        )
        new_topic.topic_tag.add(*tag_list)
        new_topic.save()
        return new_topic