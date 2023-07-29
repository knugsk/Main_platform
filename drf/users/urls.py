from django.urls import path
from .views import RegisterView, LoginView, LogoutView, UserInfoView, UserUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view(), name='logout_user'),
    path('user/', UserInfoView.as_view(), name='get_user_info'),
    path('user/update/', UserUpdateView.as_view(), name='update_user_info'),
]
