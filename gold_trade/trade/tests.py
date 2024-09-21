from rest_framework.test import APITestCase
from django.urls import reverse
from .models import User

class UserRegistrationTest(APITestCase):
    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password': 'testpass',
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 201)

    def test_register_user_invalid_data(self):
        response = self.client.post(reverse('register'), {
            'username': '',  
            'password': 'testpass',
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 400)
