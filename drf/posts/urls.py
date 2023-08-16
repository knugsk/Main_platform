from django.urls import path
from .views import CategoryPostListView, PostListView, PostDetailView, CommentListView, CommentDetailView, FileListCreateView, FileRetrieveUpdateDestroyView

urlpatterns = [
    path('categories/<int:id>/posts', CategoryPostListView.as_view(), name='category-detail'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('comments/', CommentListView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('files/', FileListCreateView.as_view(), name='file-list'),
    path('files/<int:pk>/', FileRetrieveUpdateDestroyView.as_view(), name='file-detail'),
]
urlpatterns += [
    path('posts/<int:pk>/download/', PostDetailView.as_view(), name='download-file'),
]

