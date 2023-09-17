from rest_framework import serializers
from blog.models import Post, Follow
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ("owner", "created_at", "updated_at")


class UserSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()

    def get_is_following(self, obj):
        return None

    class Meta:
        model = User
        fields = [
            "username",
            "is_following",
        ]
        read_only_fields = ("username",)


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = "__all__"
        read_only_fields = ("follower", "created_at")


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = [
            "following",
        ]
        read_only_fields = ("follower", "following", "created_at")


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = [
            "follower",
        ]
        read_only_fields = ("follower", "following", "created_at")
