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
        fields = "__all__"

class TopicSerializer(serializers.ModelSerializer):
    topic_tag = serializers.StringRelatedField(many=True)
    topic_user = serializers.CharField(source='topic_user.user_name')

    class Meta:
        model = Topic
        fields = "__all__"