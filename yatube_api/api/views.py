from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .helps import get_or_none
from .models import Comment, Follow, Group, Post
from .permissions import IsAuthorOrIsAuthenticatedOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)

User = get_user_model()


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthorOrIsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(title=self.request.data['title'])


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrIsAuthenticatedOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        group = self.request.query_params.get('group', None)
        if group is not None:
            queryset = queryset.filter(
                group=get_object_or_404(Group, id=group))
        return queryset

    def perform_create(self, serializer):
        group = get_or_none(Group, title=self.request.data.get('group'))
        serializer.save(author=self.request.user, group=group)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrIsAuthenticatedOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        queryset = super().get_queryset(*args, **kwargs).filter(post=post)
        return queryset

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs).filter(
            following=self.request.user)
        search = self.request.query_params.get('search', None)
        if search is not None:
            user = User.objects.get(username=search)
            queryset = queryset.filter(user=user)
        return queryset

    def create(self, request):
        following = get_or_none(User, username=request.data.get('following'))
        follow = Follow.objects.filter(
            user=self.request.user, following=following).exists()
        serializer = FollowSerializer(data=request.data)
        true_or_false = not follow and request.user != following and following
        if serializer.is_valid() and true_or_false:
            serializer.save(user=request.user, following=following)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
