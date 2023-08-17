from rest_framework import serializers
from .models import Category, Post, Comment, File

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'file', 'post')

class PostSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    title = serializers.CharField()
    body = serializers.CharField()
    files = FileSerializer(many=True, required=False)
    comments = CommentSerializer(many=True, read_only=True)
    author = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'category', 'author', 'title', 'body', 'files', 'comments', 'published_date']
