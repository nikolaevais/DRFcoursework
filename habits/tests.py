from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habits
from users.models import User


class HabitsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="habitstest@test.ru", password="testpassword"
        )
        self.habits = Habits.objects.create(
            user=self.user,
            location="Кухня",
            times="02:02:02",
            move="Выпить стакан воды",
            is_sign_of_pleasant_habit=False,
            periodicity="EVERYDAY",
            reward="Съешь яблоко",
            time_to_complete="00:01:59",
            is_public=True,
            next_reminde="2024-11-04",
            related_habit=None,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_habits(self):
        """Тестирование создания привычки."""
        data = {
            "user": self.user.pk,
            "location": "Ванная",
            "times": "18:10:42",
            "move": "Почистить зубы",
            "is_sign_of_pleasant_habit": False,
            "periodicity": "Everyday",
            "reward": "Выпить кофе",
            "time_to_complete": "00:02:00",
            "is_public": True,
        }
        response = self.client.post("/habits/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            response.json(),
            {
                "id": 2,
                "location": "Ванная",
                "times": "18:10:42",
                "move": "Почистить зубы",
                "is_sign_of_pleasant_habit": False,
                "periodicity": "Everyday",
                "reward": "Выпить кофе",
                "time_to_complete": "00:02:00",
                "is_public": True,
                "user": 1,
                "related_habit": None,
                "next_reminde": "2024-11-04",
            },
        )

        self.assertEqual(Habits.objects.all().count(), 2)

    def test_habits_list(self):
        """Тестирование вывода списка привычек."""
        response = self.client.get("/habits/")
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habits.pk,
                    "location": self.habits.location,
                    "times": self.habits.times,
                    "move": self.habits.move,
                    "is_sign_of_pleasant_habit": self.habits.is_sign_of_pleasant_habit,
                    "periodicity": self.habits.periodicity,
                    "reward": self.habits.reward,
                    "time_to_complete": self.habits.time_to_complete,
                    "is_public": self.habits.is_public,
                    "user": self.user.pk,
                    "next_reminde": "2024-11-04",
                    "related_habit": None,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_public_habits(self):
        """Тестирование вывода публичных привычек."""
        data = {
            "user": self.user.pk,
            "location": "Зал",
            "times": "18:15:42",
            "move": "Зарядка",
            "is_sign_of_pleasant_habit": False,
            "periodicity": "Everyday",
            "reward": "Съесть яблоко",
            "time_to_complete": "00:02:00",
            "is_public": False,
        }
        response = self.client.post("/habits/", data=data)
        response1 = self.client.get(reverse("habits:habits_public"))
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 1)

    def test_habits_update(self):
        url = reverse("habits:habits-detail", args=(self.habits.pk,))
        data = {"move": "Зарядка"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("move"), "Зарядка")

    def test_lesson_delete(self):
        """Тестирование удаление привычки."""
        url = reverse("habits:habits-detail", args=[self.habits.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habits.objects.all().count(), 0)

    def test_owner_permission(self):
        """Тестирование удаление привычки только владельцем."""
        another_user = User.objects.create(email="anotheruser", password="testpassword")
        self.client.force_authenticate(user=another_user)
        response = self.client.delete(
            reverse("habits:habits-detail", args=[self.habits.id])
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_habits_create_prohibit_filling(self):
        """Тестирование запрета создания привычки с валидацией на одновременное заполнение двух полей вознаграждение и связанная привычка"""

        data = {
            "user": self.user.pk,
            "location": "Зал",
            "times": "18:15:42",
            "move": "Зарядка",
            "is_sign_of_pleasant_habit": True,
            "periodicity": "Everyday",
            "time_to_complete": "00:02:00",
            "is_public": False,
        }
        response = self.client.post("/habits/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data1 = {
            "user": self.user.pk,
            "location": "Ванная",
            "times": "18:10:42",
            "move": "Почистить зубы",
            "is_sign_of_pleasant_habit": False,
            "periodicity": "Everyday",
            "reward": "Выпить кофе",
            "time_to_complete": "00:02:00",
            "is_public": True,
            "related_habit": response.data["id"],
        }

        response1 = self.client.post("/habits/", data=data1)

        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response1.json(),
            {
                "non_field_errors": [
                    'Поля "Вознаграждение" и "Связанная привычка" не могут быть заполнены одновременно. Заполните одно поле'
                ]
            },
        )

    def test_habits_create_valid_filling(self):
        """Тестирование создания привычки с валидацией на одновременное заполнение двух полей вознаграждение и связанная привычка"""

        data = {
            "user": self.user.pk,
            "location": "Зал",
            "times": "18:15:42",
            "move": "Зарядка",
            "is_sign_of_pleasant_habit": True,
            "is_public": False,
        }
        response = self.client.post("/habits/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data1 = {
            "user": self.user.pk,
            "location": "Улица",
            "times": "18:15:42",
            "move": "Прогулка",
            "is_sign_of_pleasant_habit": False,
            "periodicity": "Everyday",
            "time_to_complete": "00:02:00",
            "is_public": True,
            "related_habit": response.data["id"],
        }

        response1 = self.client.post("/habits/", data=data1)

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habits.objects.all().count(), 3)

    def test_habits_create_prohibit_filling(self):
        """Тестирование запрета создания привычки с валидацией на то, что время выполнения привычки не может быть больше 2 минут"""

        data = {
            "user": self.user.pk,
            "location": "Спортзал",
            "times": "18:15:42",
            "move": "Штанга",
            "reward": "Съесть банан",
            "is_sign_of_pleasant_habit": False,
            "periodicity": "Everyday",
            "time_to_complete": "00:02:05",
            "is_public": True,
        }

        response = self.client.post("/habits/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Время на выполнение привычки не может быть больше 2 минут"
                ]
            },
        )

    def test_habits_create_valid_filling(self):
        """Тестирование создания привычки с валидацией на то, что время выполнения привычки не может быть больше 2 минут"""

        data = {
            "user": self.user.pk,
            "location": "Спортзал",
            "times": "18:15:42",
            "move": "Штанга",
            "reward": "Съесть банан",
            "is_sign_of_pleasant_habit": False,
            "periodicity": "Everyday",
            "time_to_complete": "00:02:00",
            "is_public": True,
        }

        response = self.client.post("/habits/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habits.objects.all().count(), 2)

    def test_habits_create_prohibit_related(self):
        """Тестирование запрета создания привычки с валидацией на то, что в связанные привычки могут попадать только привычки с признаком приятной привычки."""

        data = {
            "user": self.user.pk,
            "location": "Улица",
            "times": "18:15:42",
            "move": "Прогулка",
            "is_sign_of_pleasant_habit": False,
            "periodicity": "Everyday",
            "time_to_complete": "00:02:00",
            "is_public": True,
            "related_habit": self.habits.pk,
        }

        response = self.client.post("/habits/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {"non_field_errors": ["Связанная привычка должна быть приятной привычкой"]},
        )

    def test_habits_create_prohibit_related(self):
        """Тестирование создания привычки с валидацией на то, что в связанные привычки могут попадать только привычки с признаком приятной привычки."""

        data = {
            "user": self.user.pk,
            "location": "Зал",
            "times": "18:20:42",
            "move": "Зарядка",
            "is_sign_of_pleasant_habit": True,
            "is_public": False,
        }

        response = self.client.post("/habits/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data1 = {
            "user": self.user.pk,
            "location": "Улица",
            "times": "18:15:42",
            "move": "Прогулка",
            "is_sign_of_pleasant_habit": False,
            "periodicity": "Everyday",
            "time_to_complete": "00:02:00",
            "is_public": True,
            "related_habit": response.data["id"],
        }

        response1 = self.client.post("/habits/", data=data1)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habits.objects.all().count(), 3)

    def test_habits_create_prohibit_re(self):
        """Тестирование запрета создания привычки с валидацией на то, что у приятной привычки не может быть вознаграждения или  связанной привычки"""

        data = {
            "user": self.user.pk,
            "location": "Спортзал",
            "times": "18:30:42",
            "move": "Приседания",
            "is_sign_of_pleasant_habit": True,
            "is_public": False,
        }

        response = self.client.post("/habits/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data1 = {
            "user": self.user.pk,
            "location": "Улица",
            "times": "18:15:42",
            "move": "Отдых на скамейки",
            "is_sign_of_pleasant_habit": True,
            "periodicity": "Everyday",
            "time_to_complete": "00:02:00",
            "is_public": True,
            "related_habit": response.data["id"],
        }

        response1 = self.client.post("/habits/", data=data1)

        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response1.json(),
            {
                "non_field_errors": [
                    "У приятной привычки не может быть вознаграждения или связанной привычки"
                ]
            },
        )

        data2 = {
            "user": self.user.pk,
            "location": "Улица",
            "times": "18:15:42",
            "move": "Отдых на скамейки",
            "is_sign_of_pleasant_habit": True,
            "reward": "Съесть банан",
            "periodicity": "Everyday",
            "time_to_complete": "00:02:00",
            "is_public": True,
        }

        response2 = self.client.post("/habits/", data=data2)

        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response2.json(),
            {
                "non_field_errors": [
                    "У приятной привычки не может быть вознаграждения или связанной привычки"
                ]
            },
        )
