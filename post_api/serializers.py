from rest_framework import serializers
from post_api import models


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ['id', 'image']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ['id', 'author', 'text', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Like
        fields = ['id', 'user', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    comments = CommentSerializer(many=True, source='post_comments')
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Post
        fields = [
            'id',
            'author',
            'text',
            'created_at',
            'images',
            'comments',
            'likes_count'
        ]
