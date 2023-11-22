from django.shortcuts import render
from .models import Post
from django.http import HttpResponse
from blog.serializers import PostSerializer
from django.shortcuts import get_object_or_404
# django rest framework. DRF
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response

# Create your views here.
    
    
class BlogView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    #handle exceptions
    class BlogException(APIException):
        status_code = 405
        default_detail = {
            "code": status_code,
            "message": "Unable to load the available blogs. Or they are no Blogs available",
        }
    @action(detail=True, methods=["get", "post"])
    def blogs(self, request, pk):
        blog = get_object_or_404(Post, id=pk)

        if blog.available_count > 1:
            # Return all available blogs
            blogs = Post.objects.all()
            serializer = self.get_serializer(blogs, many=True)
            return Response(serializer.data)
        elif brand.available_count == 1:
            # Return only the selected blog
            serializer = self.get_serializer(blog)
            return Response(serializer.data)
        else:
            # No available listed blogs
            raise self.BlogException
    

