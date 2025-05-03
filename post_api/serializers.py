from rest_framework import serializers
from post_api import models


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ['id', 'image']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = models.Comment
        fields = ['id', 'author', 'text', 'created_at']
        read_only_fields = ['author', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
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


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    new_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False),
        write_only=True,
        required=False
    )
    delete_images = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = models.Post
        fields = ['text', 'new_images', 'delete_images']

    def create(self, validated_data):
        images_data = validated_data.pop('new_images', [])
        post = models.Post.objects.create(
            author=self.context['request'].user,
            **validated_data
        )
        models.Image.objects.bulk_create(
            [models.Image(post=post, image=image) for image in images_data]
        )
        return post

    def update(self, instance, validated_data):
        delete_ids = validated_data.pop('delete_images', [])
        instance.images.filter(id__in=delete_ids, post=instance).delete()

        images_data = validated_data.pop('new_images', [])
        models.Image.objects.bulk_create(
            [models.Image(post=instance, image=image) for image in images_data]
        )

        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance
