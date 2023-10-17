from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            # Add other required fields here
        }

    def test_register_user_success(self):
        url = reverse('register')  # Use the name of the URL pattern for registration
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_existing_email(self):
        # Create a user with the same email
        user = get_user_model().objects.create_user(**self.user_data)
        url = reverse('register')  # Use the name of the URL pattern for registration
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_invalid_data(self):
        # Test invalid data scenarios
        invalid_data = {
            'email': 'invalid_email',  # Invalid email format
            'password': '',  # Password is required
        }
        url = reverse('register')  # Use the name of the URL pattern for registration
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserLoginTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "email": "newuser@example.com",
            "password": "string",
        }
        # Create a user for login testing
        self.user = get_user_model().objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password']
        )
        print("PASSWORD", self.user.password)

    def test_user_login_success(self):
        url = reverse('login')  # Use the name of the URL pattern for login
        response = self.client.post(url, self.user_data, format='json')
        print("PRINTED", response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_invalid_password(self):
        invalid_data = {
            "email": self.user_data['email'],
            "password": "invalid_password",
        }
        url = reverse('login')  # Use the name of the URL pattern for login
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Invalid password', response.data['error'])

    def test_user_login_user_not_found(self):
        non_existing_email = "non_existing_user@example.com"
        data = {
            "email": non_existing_email,
            "password": "some_password",
        }
        url = reverse('login')  # Use the name of the URL pattern for login
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('User not found', response.data['error'])
