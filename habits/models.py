from django.db import models

from config import settings
from users.models import NULLABLE


class Habits(models.Model):
    PERIOD_DAY = [
        ('EVERYDAY', 'каждый день'),
        ('EVERYWEEK', 'раз в неделю'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Создатель привычки")
    location = models.CharField(max_length=250, verbose_name="Место")
    times = models.TimeField(verbose_name="Время, когда необходимо выполнить привычку")
    move = models.CharField(max_length=250, verbose_name="Действие")
    is_sign_of_pleasant_habit = models.BooleanField(default=False, verbose_name="Признак приятной привычки")
    related_habit = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name="Связанная привычка", **NULLABLE)
    periodicity = models.CharField(max_length=50, default="EVERYDAY", verbose_name="Периодичность", choices=PERIOD_DAY)
    reward = models.CharField(max_length=250, verbose_name="Вознаграждение", **NULLABLE)
    time_to_complete = models.DurationField(verbose_name="Время на выполнение привычки", **NULLABLE)
    is_public = models.BooleanField(default=False, verbose_name="Видно всем")

    def __str__(self):
        return self.move

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
