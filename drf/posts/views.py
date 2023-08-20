import boto3
import botocore.exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
import boto3
import botocore
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status



from rest_framework.exceptions import PermissionDenied

from rest_framework.decorators import action
from rest_framework import status

S3_BUCKET_NAME = 'bucket-xgthnf'
S3_REGION_NAME = 'ap-northeast-2'

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

                serializer.save(author=user, category=category, title=title, body=body)
                File.objects.create(file=file_data, post=serializer.instance)


from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import Post, Category
from .serializers import PostSerializer
from .permissions import IsAuthorOrStaffOrAdmin

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrStaffOrAdmin]

    def perform_update(self, serializer):
        category_name = self.request.data.get('category')
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            return Response("잘못된 카테고리 이름입니다.", status=status.HTTP_400_BAD_REQUEST)

        serializer.save(category=category)

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

    def perform_destroy(self, instance):
        instance.file.delete()  # 연결된 파일 삭제
        instance.delete()  # 파일 인스턴스 삭제
        return Response(status=status.HTTP_204_NO_CONTENT)
    
import boto3
import botocore.exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import boto3
import botocore

class FileDownloadView(APIView):
    def get(self, request, *args, **kwargs):
        filename_with_extension = kwargs.get('filename')  # 파일 이름과 확장자
        s3_client = boto3.client('s3', region_name=S3_REGION_NAME)  # bucket 인자를 제거하고 s3_client 초기화
        
        try:
            # 파일 다운로드
            local_file_path = '' + filename_with_extension
            s3_client.download_file(S3_BUCKET_NAME, filename_with_extension, local_file_path)
            
            response = Response("파일 다운로드 성공.", status=status.HTTP_200_OK)
            
            # Content-Disposition 헤더 추가
            response['Content-Disposition'] = 'attachment;'
            
            return response
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                return Response("파일을 찾을 수 없습니다.", status=status.HTTP_404_NOT_FOUND)
            else:
                return Response("파일 다운로드 중에 오류가 발생했습니다.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FileUploadView(generics.CreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthorOrStaffOrAdmin]

    def perform_create(self, serializer):
        post_id = self.request.data.get('post_id')
        serializer.save(post_id=post_id)
        return Response("파일 업로드 성공.", status=status.HTTP_201_CREATED)
