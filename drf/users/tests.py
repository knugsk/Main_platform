from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

class LogoutTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            stu_id='testuser',
            first_name='Test',
            last_name='User',
            password='testpassword',
        )

    def test_logout(self):
        # 로그인 시도
        login_url = '/login/'
        login_data = {'stu_id': 'testuser', 'password': 'testpassword'}
        login_response = self.client.post(login_url, login_data, format='json')

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('token', login_response.data)

        # 로그아웃 시도
        logout_url = '/logout/'  # 패턴 이름 대신 URL 문자열 사용
        logout_response = self.client.delete(logout_url, format='json')

        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        self.assertEqual(logout_response.data, {'detail': '성공적으로 로그아웃되었습니다.'})

        # 다시 로그인 시도 (로그아웃으로 인증 토큰이 삭제되었으므로 실패해야 함)
        login_response = self.client.post(login_url, login_data, format='json')

        self.assertEqual(login_response.status_code, status.HTTP_401_UNAUTHORIZED)
