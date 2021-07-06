from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .helps import get_or_none
from .models import Comment, Follow, Group, Post
from .permissions import IsAuthorOrIsAuthenticatedOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)

User = get_user_model()


class GroupViewSet(viewsets.ModelViewSet,
                   mixins.CreateModelMixin,
                   mixins.ListModelMixin):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthorOrIsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(title=self.request.data['title'])


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrIsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('group', )

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


class FollowViewSet(viewsets.ModelViewSet,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'following__username', ]

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset.filter(following=self.request.user)

    # def perform_create(self, serializer):
    #     following = get_or_none(
    #         User, username=self.request.data.get('following')
    #     )
    #     serializer.save(user=self.request.user, following=following)

    # Пытался сделать все красиво, но pytest не пропускает из-за serializers
    # Также не могу понять, правильно ли я сделал с CheckConstraint в models
    # Уже все перепробовал, но так же могу подписываться на самого себя =(
    def create(self, request):
        serializer = FollowSerializer(data=request.data)
        following = get_or_none(
            User, username=request.data.get('following')
        )
        follow = Follow.objects.filter(
            user=request.user, following=following
        ).exists()
        if serializer.is_valid() and not follow and request.user != following:
            serializer.save(user=request.user, following=following)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
