from django.urls import path, include
from rest_framework.routers import DefaultRouter
from post_api import views

router = DefaultRouter()
router.register('posts', views.PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls))
]
