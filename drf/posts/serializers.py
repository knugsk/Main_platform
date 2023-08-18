from rest_framework import serializers
from .models import Category, Post, Comment, File
from users.models import CustomUser

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'file', 'post')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser 
        fields = ('first_name', 'last_name')


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    parent_comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), allow_null=True, required=False)
    class Meta:
        model = Comment
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    title = serializers.CharField()
    body = serializers.CharField()
    files = FileSerializer(many=True, required=False)
    comments = CommentSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'category', 'author', 'title', 'body', 'files', 'comments', 'published_date']

