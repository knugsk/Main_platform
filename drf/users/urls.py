# 프로젝트의 urls.py 파일

from django.urls import path, include
from .views import RegisterView, LoginView, LogoutView, UserInfoView, UserUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view(), name='logout_user'),  # LogoutView에 대한 URL 패턴을 등록
    path('user/<int:pk>', UserInfoView.as_view(), name='get_user_info'),
    path('user/update/', UserUpdateView.as_view(), name='update_user_info'),
]
