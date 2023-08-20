from django.urls import path
from .views import CategoryPostListView, PostListView, PostDetailView, CommentCreateView, CommentReplyCreateView, FileRetrieveUpdateDestroyView, CommentUpdateView
from .views import FileUploadView, FileDownloadView

urlpatterns = [
    path('categories/<int:id>/posts', CategoryPostListView.as_view(), name='category-detail'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:parent_comment_id>/replies/', CommentReplyCreateView.as_view(), name='comment-reply-create'),
    path('comments/<int:pk>/', CommentUpdateView.as_view(), name='comment-update-delete'),
    path('files/<int:pk>/', FileRetrieveUpdateDestroyView.as_view(), name='file-download'),
    path('file/<str:file_name>', FileDownloadView.as_view(), name='file-download'),
    path('reupload/', FileUploadView.as_view(), name='file-upload'),
]