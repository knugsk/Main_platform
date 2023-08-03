from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .serializers import LoginSerializer, CustomUserSerializer, UserSerializer, UserUpdateSerializer
from rest_framework.exceptions import NotFound

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        token, created = Token.objects.get_or_create(user=data['user'])
        return Response({"token": token.key}, status=status.HTTP_200_OK)

class LogoutView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
        except Token.DoesNotExist:
            pass

        return Response({"detail": "성공적으로 로그아웃되었습니다."}, status=status.HTTP_200_OK)


class UserInfoView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user
