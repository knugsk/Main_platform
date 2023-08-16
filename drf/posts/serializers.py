from rest_framework import serializers
from .models import Category, Post, Comment, File

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'file', 'post')

class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    files = FileSerializer(many=True, required=False)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
