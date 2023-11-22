from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogView

router = DefaultRouter()
router.register(r'posts', BlogView, basename='blog')

urlpatterns = [
    path('', include(router.urls)),
]
