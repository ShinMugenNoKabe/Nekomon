from rest_framework import serializers

from nekomon.models import User, Post


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%d/%m/%Y")

    class Meta:
        model = User
        fields = ["username", "name", "description", "profile_picture", "date_joined"]


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M")
    username = serializers.CharField(source="user.username")
    profile_picture = serializers.CharField(source="user.profile_picture")

    class Meta:
        model = Post

        fields = ["id", "content", "image", "username", "profile_picture", "created_at"]
