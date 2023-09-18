import uuid

import boto3
from django.core.files.base import File
from django.conf import settings
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.request import Request
from django.contrib.auth.models import User
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from .models import Post, Follow
from .serializers import (
    PostSerializer,
    PostUploadSerializer,
    FollowSerializer,
    UserSerializer,
    FollowerSerializer,
    FollowingSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(is_hidden=False)
    serializer_class = PostSerializer

    @action(detail=False, methods=["get"], url_name="my_post")
    def my_post(self, request: Request, *args, **kwargs):
        user = request.user
        obj = Post.objects.filter(owner=user)
        serializer = PostSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_name="following_post")
    def following_post(self, request: Request, *args, **kwargs):
        user = request.user
        follow = Follow.objects.filter(follower=user)
        serializer = FollowSerializer(follow, many=True)
        following_list = []
        for data in serializer.data:
            following_list.append(data["following"])

        obj = Post.objects.filter(owner__in=following_list, is_hidden=False)
        serializer = PostSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def list(self, request, *args, **kwargs):
    #     obj = Post.objects.filter(is_hidden=False)
    #     serializer = PostSerializer(obj, many=True)
    #     return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "create":
            return PostUploadSerializer
        return super().get_serializer_class()

    def create(self, request: Request, *args, **kwargs):
        title = request.data.get("title")
        body = request.data.get("body")
        is_hidden = request.data.get("is_hidden")

        if image := request.data.get("image"):
            image: File
            service_name = "s3"
            endpoint_url = "https://kr.object.ncloudstorage.com"
            access_key = settings.NCP_ACCESS_KEY
            secret_key = settings.NCP_SECRET_KEY
            bucket_name = "post-image-jy"

            s3 = boto3.client(
                service_name,
                endpoint_url=endpoint_url,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
            )

            # s3 upload
            image_id = str(uuid.uuid4())
            ext = image.name.split(".")[-1]
            image_filename = f"{image_id}.{ext}"
            s3.upload_fileobj(image.file, bucket_name, image_filename)

            # get image url
            s3.put_object_acl(
                ACL="public-read",
                Bucket=bucket_name,
                Key=image_filename,
            )
            image_url = f"{endpoint_url}/{bucket_name}/{image_filename}"

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            data["owner"] = request.user
            data["image_url"] = image_url if image else None
            res: Post = Post.objects.create(**data)
            return Response(
                status=status.HTTP_201_CREATED, data=PostSerializer(res).data
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def retrieve(self, request: Request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request: Request, *args, **kwargs):
        user = request.user
        post: Post = self.get_object()
        if not post.access_by_post(user):
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="Unauthorized")

        return super().destroy(request, *args, **kwargs)

    def update(self, request: Request, *args, **kwargs):
        user = request.user
        post: Post = self.get_object()
        if not post.access_by_post(user):
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="Unauthorized")
        return super().update(request, *args, **kwargs)

    @extend_schema(deprecated=True)
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_400_BAD_REQUEST, data="Deprecated API")


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request: Request, *args, **kwargs):
        obj = User.objects.exclude(username=request.user)
        serializer = UserSerializer(obj, many=True)
        for data in serializer.data:
            data["is_following"] = Follow.objects.filter(
                follower=request.user,
                following=User.objects.get(username=data["username"]),
            ).exists()
        return Response(serializer.data)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    @action(detail=False, methods=["get"], url_name="follower")
    def follower(self, request: Request, *args, **kwargs):
        follower = request.user
        obj = Follow.objects.filter(follower=follower)
        serializer = FollowerSerializer(obj, many=True)
        for data in serializer.data:
            data["following"] = User.objects.get(id=data["following"]).username

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_name="following")
    def following(self, request: Request, *args, **kwargs):
        following = request.user
        obj = Follow.objects.filter(following=following)
        serializer = FollowingSerializer(obj, many=True)
        for data in serializer.data:
            data["follower"] = User.objects.get(id=data["follower"]).username

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request, *args, **kwargs):
        follower = request.user
        following = User.objects.get(id=request.data.get("following"))
        follow, created = Follow.objects.get_or_create(
            follower=follower, following=following
        )
        serializer = FollowSerializer(follow)
        if not created:
            return Response(status=status.HTTP_409_CONFLICT)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request: Request, *args, **kwargs):
        follower = request.user
        following = User.objects.get(username=kwargs["username"])
        follow = Follow.objects.get(follower=follower, following=following)
        follow.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
