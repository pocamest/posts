from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)
from post_api import serializers, models
from .permissions import IsAuthorOrReadOnly
from django.db.models import Count


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PostSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
    queryset = (
        models.Post.objects
        .annotate(likes_count=Count('post_likes'))
        .select_related('author')
        .prefetch_related('images', 'post_comments', 'post_likes')
    )

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return serializers.PostCreateUpdateSerializer
        return super().get_serializer_class()

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated],
        url_path='like'
    )
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        like, created = models.Like.objects.get_or_create(user=user, post=post)

        if not created:
            like.delete()

        likes_count = models.Like.objects.filter(post=post).count()

        return Response({
            'is_liked': created,
            'likes_count': likes_count
        }, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return models.Comment.objects.filter(
            post_id=self.kwargs['post_pk']
        ).select_related('author')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post_id=self.kwargs['post_pk']
        )
