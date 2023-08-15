from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Category, Post, Comment, File
from .serializers import CategorySerializer, PostSerializer, CommentSerializer, FileSerializer
from .permissions import IsStaffOrAdminWriteOnly, IsAuthorOrStaffOrAdmin
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from rest_framework.decorators import action
from rest_framework import status

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated | IsStaffOrAdminWriteOnly]

    def perform_create(self, serializer):
        category_id = self.request.data.get('category')
        category = Category.objects.get(pk=category_id)

        if category.name in ['notice', 'closed']:
            if not self.request.user.is_staff and not self.request.user.is_superuser:
                return Response("You are not authorized to create posts in this category.", status=status.HTTP_403_FORBIDDEN)

        serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrStaffOrAdmin]
 # 하나의 파일을 다운로드하는 액션 추가
    @action(detail=True, methods=['GET'])
    def download_file(self, request, pk=None):
        post = self.get_object()
        file_id = request.GET.get('file_id')  # 요청의 쿼리 파라미터로 file_id를 받아옵니다.
        file = get_object_or_404(File, id=file_id, post=post)

        if file:
            response = FileResponse(file.file, as_attachment=True)
            return response
        else:
            return Response("파일이 존재하지 않습니다.", status=status.HTTP_404_NOT_FOUND)
        

class CommentListView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated | IsStaffOrAdminWriteOnly]

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrStaffOrAdmin]

class FileListCreateView(generics.ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer

class FileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer