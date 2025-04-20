from django.shortcuts import render
from rest_framework import viewsets
from post_api import serializers, models


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PostSerializer
    queryset = models.Post.objects.all()
