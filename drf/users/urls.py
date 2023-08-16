# 프로젝트의 urls.py 파일

from django.urls import path, include
from .views import RegisterView, LoginView, LogoutView, UserInfoView
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view(), name='logout_user'),  # LogoutView에 대한 URL 패턴을 등록
    path('<str:pk>', UserInfoView.as_view(), name='get_user_info'),
]