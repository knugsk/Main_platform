from django.test import TestCase
from .models import CustomUser

from rest_framework.test import APIClient
from rest_framework import status

class ModelTest(TestCase):
    def setUp(self):
        self.stu_id = "0000000000"
        self.first_name = "te"
        self.last_name = "st"


class ViewTest(TestCase):
    def setUp(self):
            self.client = APIClient()
            self.userdata = {'stu_id': '0000000000', 'first_name': 'te', 'last_name' : 'st', 'password' : 'testroot', 'password2':'testroot'}
            self.response = self.client.post('/users/register',
                                            self.userdata,
                                            format="json")

    def test_api_can_create_a_book(self):
        print(self.response.content)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)