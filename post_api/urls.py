from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from post_api import views

router = DefaultRouter()
router.register('posts', views.PostViewSet)

posts_router = NestedDefaultRouter(router, 'posts', lookup='post')
posts_router.register(
    'comments',
    views.CommentViewSet,
    basename='post-comments'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(posts_router.urls))
]
