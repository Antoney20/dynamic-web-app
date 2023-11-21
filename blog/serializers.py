import json

from rest_framework import serializers
from blog.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        Model = Post
        fields =[
            'id',
            'title',
            'image',
            'body',
            'created_at',        
        ]
