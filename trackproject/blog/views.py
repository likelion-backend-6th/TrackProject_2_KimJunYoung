from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.request import Request
from django.contrib.auth.models import User


from .models import Post, Follow
from .serializers import PostSerializer, UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request: Request, *args, **kwargs):
        title = request.data.get("title")
        body = request.data.get("body")
        owner = request.user
        post = Post.objects.create(title=title, body=body, owner=owner)
        serializer = PostSerializer(post)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request: Request, *args, **kwargs):
        user = request.user
        post: Post = self.get_object()
        if not post.access_by_post(user):
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="Unauthorized")
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        post: Post = self.get_object()
        if not post.access_by_post(user):
            return Response(status=status.HTTP_401_UNAUTHORIZED, data="Unauthorized")

        return super().destroy(request, *args, **kwargs)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request: Request, *args, **kwargs):
        obj = User.objects.exclude(username=request.user)
        serializer = UserSerializer(obj, many=True)
        return Response(serializer.data)
