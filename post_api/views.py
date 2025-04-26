from django.shortcuts import render
from rest_framework import viewsets
from post_api import serializers, models
from .permissions import IsAuthorOrReadOnly
from django.db.models import Count


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        return models.Post.objects.annotate(
            likes_count=Count('post_likes')
        ).select_related('author').prefetch_related('images', 'post_comments')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
