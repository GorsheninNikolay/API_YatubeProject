from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Comment, Follow, Group, Post
from .permissions import IsAuthorOrIsAuthenticatedOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)

User = get_user_model()


"""
Спасибо огромное!!! Все получилось. Все действительно было из-за serializers
Особенно помогло обсуждение в слаке default=serializers.CurrentDefaultUser()
Но много странствовал по разным сайтам, но этого нигде не нашел...
Почему именно так сработало? Можно ли где-то подробнее про это почитать?
Заранее огромное спасибо =)
"""


class CreateListSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    pass


class GroupViewSet(CreateListSet):
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
        serializer.save(author=self.request.user)


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


class FollowViewSet(CreateListSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'following__username', ]

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset.filter(following=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
