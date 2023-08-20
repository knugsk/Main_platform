from django.urls import path
from .views import CategoryPostListView, PostListView, PostDetailView, CommentCreateView, CommentReplyCreateView, FileListCreateView, FileRetrieveUpdateDestroyView, CommentUpdateView
from .views import S3ProxyView
urlpatterns = [
    path('categories/<int:id>/posts', CategoryPostListView.as_view(), name='category-detail'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:parent_comment_id>/replies/', CommentReplyCreateView.as_view(), name='comment-reply-create'),
    path('comments/<int:pk>/', CommentUpdateView.as_view(), name='comment-update-delete'),
    path('files/<int:pk>/', FileRetrieveUpdateDestroyView.as_view(), name='file-detail'),
    # path('posts/<int:file_id>/download', S3ProxyView.as_view(), name='s3-proxy'),

]