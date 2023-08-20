from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Category, Post, Comment, File
from .serializers import CategorySerializer, PostSerializer, CommentSerializer, FileSerializer
from .permissions import IsStaffOrAdminWriteOnly, IsAuthorOrStaffOrAdmin
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


from rest_framework.exceptions import PermissionDenied

from rest_framework.decorators import action
from rest_framework import status
from drf.settings import prod

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

    def perform_update(self, serializer):
        files_data = self.request.FILES.getlist('files')
        post_id = self.kwargs.get('pk')  # 게시물 ID 가져오기

        if files_data and post_id:
            for file_data in files_data:
                file_instance = File(file=file_data, post_id=post_id)
                file_instance.save()

        serializer.save()

    def perform_destroy(self, instance):
        instance.file.delete()  # 연결된 파일 삭제
        instance.delete()  # 파일 인스턴스 삭제
        return Response(status=status.HTTP_204_NO_CONTENT)



import boto3
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FileModel

class LightsailBucketFileDownloadView(APIView):
    def get_object(self, file_id):
        try:
            return FileModel.objects.get(id=file_id)
        except FileModel.DoesNotExist:
            raise Http404

    def get(self, request, file_id, format=None):
        file_obj = self.get_object(file_id)

        # AWS Lightsail 버킷에 접근하기 위해 boto3 클라이언트 생성
        s3 = boto3.client(
            's3',
            endpoint_url='bucket-xgthnf.s3.ap-northeast-2.amazonaws.com',  # Lightsail 버킷 엔드포인트 URL
        )

        try:
            # Lightsail 버킷에서 파일 데이터 가져오기
            response = s3.get_object(
                Bucket='YOUR_BUCKET_NAME',  # Lightsail 버킷 이름
                Key=file_obj.file_field.name  # 파일 필드 이름
            )
            file_content = response['Body'].read()
            content_type = response['ContentType']

            # 파일 다운로드 응답 생성
            download_response = Response(file_content, content_type=content_type)
            download_response['Content-Disposition'] = f'attachment; filename="{file_obj.original_filename}"'
            return download_response
        except Exception as e:
            raise Http404
