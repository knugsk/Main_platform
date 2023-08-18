from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Category, Post, Comment, File
from .serializers import CategorySerializer, PostSerializer, CommentSerializer, FileSerializer
from .permissions import IsStaffOrAdminWriteOnly, IsAuthorOrStaffOrAdmin
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

import os
import uuid


from rest_framework.exceptions import PermissionDenied

from rest_framework.decorators import action
from rest_framework import status

class CategoryRetrieveView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

class CategoryPostListView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        category_id = self.kwargs['id']
        return Post.objects.filter(category_id=category_id)
from rest_framework.authtoken.models import Token

class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated | IsStaffOrAdminWriteOnly]

    def perform_create(self, serializer):
        category_name = self.request.data.get('category')
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            raise Response("잘못된 카테고리 이름입니다.", status=status.HTTP_400_BAD_REQUEST)

        title = self.request.data.get('title')
        body = self.request.data.get('body')

        # 사용자의 토큰을 이용하여 현재 사용자 정보를 가져옴
        token_key = self.request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token = Token.objects.get(key=token_key)
        user = token.user

        if (category.name == 'notice' or category.name == 'closed') and (not user.is_staff or not user.is_superuser):
            raise PermissionDenied("이 카테고리에 글을 작성할 권한이 없습니다.", code=403)
        else:
            
            files_data = self.request.FILES.getlist('files')  # 업로드된 파일 목록 가져오기

            serializer.save(author= user, category=category, title=title, body=body)

            # 파일 정보 저장
            for file_data in files_data:
                file_name = f"{serializer.instance.id}-{file_data.name}"

                file_instance = File(file=file_name, post=serializer.instance)
                file_instance.save()

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrStaffOrAdmin]

    # 수정 기능 추가 (이전 설명 참고)
    def perform_update(self, serializer):
        category_name = self.request.data.get('category')
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            return Response("잘못된 카테고리 이름입니다.", status=status.HTTP_400_BAD_REQUEST)

        serializer.save(category=category)
        
    # 파일 다운로드 액션 유지 (이전 설명 참고)
    @action(detail=True, methods=['GET'])
    def download_file(self, request, pk=None):
        post = self.get_object()
        file_id = request.GET.get('file_id')
        file = get_object_or_404(File, id=file_id, post=post)

        if file:
            response = FileResponse(file.file, as_attachment=True)
            return response
        else:
            return Response("파일이 존재하지 않습니다.", status=status.HTTP_404_NOT_FOUND)

    # 삭제 기능 추가
    def perform_destroy(self, instance):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrStaffOrAdmin]

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.author == self.request.user or self.request.user.is_staff or self.request.user.is_admin:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to update this comment.")

    def perform_destroy(self, instance):
        if instance.author == self.request.user or self.request.user.is_staff or self.request.user.is_admin:
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete this comment.")


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        token_key = self.request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token = Token.objects.get(key=token_key)
        user = token.user
        serializer.save(author=user)

class CommentReplyCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        parent_comment_id = self.kwargs.get('parent_comment_id')
        parent_comment = Comment.objects.get(pk=parent_comment_id)

        token_key = self.request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token = Token.objects.get(key=token_key)
        user = token.user

        serializer.save(author=user, parent_comment=parent_comment)

class FileListCreateView(generics.ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer

class FileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer