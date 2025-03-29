import os
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='posts'
    )
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username}: {self.text[:30]}...'


class Photo(models.Model):
    post = models.ForeignKey(
        to=Post, on_delete=models.CASCADE, related_name='photos'
    )
    image = models.ImageField(upload_to='photos/')

    def __str__(self):
        filename = os.path.basename(self.image.name)
        return f'{self.post}: {filename}'
