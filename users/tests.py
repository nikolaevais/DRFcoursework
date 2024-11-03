from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from users.models import User


class UserTests(TestCase):
    def setUp(self):
        self.user = {
            "email": "testuser@example.com",
            "password": "testpassword",
            "phone": "1234567890",
            "city": "Test City",
            "tg_chat_id": "12345",
        }

    def test_user_registration(self):
        """Тест регистрации нового пользователя."""
        response = self.client.post(reverse("users:register"), self.user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, self.user["email"])

    def test_user_registration_without_email(self):
        """Тест регистрации без указания email."""
        data = self.user
        data["email"] = ""
        response = self.client.post(reverse("users:register"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_without_password(self):
        """Тест регистрации без указания пароля"""
        data = self.user
        data["password"] = ""
        response = self.client.post(reverse("users:register"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        """Тест входа пользователя"""
        self.client.post(reverse("users:register"), self.user)

        # Теперь пробуем войти
        login_data = {"email": self.user["email"], "password": self.user["password"]}
        response = self.client.post(reverse("users:login"), login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_user_login_invalid_credentials(self):
        """Тест входа с неверными учетными данными"""
        login_data = {"email": "123", "password": "123"}
        response = self.client.post(reverse("users:login"), login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
