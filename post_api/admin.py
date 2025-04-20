from django.contrib import admin
from .models import Image, Post


class ImageInline(admin.TabularInline):
    model = Image


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created_at')
    inlines = [ImageInline]
