from django.db import models

from config import settings
from users.models import NULLABLE


class Habits(models.Model):
    ED = 'every day"'
    EOD = 'every other day'
    OETD = 'once every three days'
    OEFD = 'once every four days'
    OEFiD = 'once every five days'
    OESD = 'once every six days'
    OW = 'once a week'

    PERIOD: [
        ("ED", "каждый день"),
        ("EOD", "через день"),
        ("OETD", "раз в три дня"),
        ("OEFD", "раз в четыре дня"),
        ("OEFiD", "раз в пять дня"),
        ("OESD", "раз в шесть дней"),
        ("OW", "раз в неделю"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Создатель привычки")
    location = models.CharField(max_length=250, verbose_name="Место")
    times = models.TimeField(verbose_name="Время, когда необходимо выполнить привычку")
    move = models.CharField(max_length=250, verbose_name="Действие")
    is_sign_of_pleasant_habit = models.BooleanField(default=False, verbose_name="Признак приятной привычки")
    related_habit = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name="Связанная привычка")
    periodicity = models.CharField(max_length=50, default=ED, verbose_name="Периодичность", choices=PERIOD, **NULLABLE)
    reward = models.CharField(max_length=250, verbose_name="Вознаграждение", **NULLABLE)
    time_to_complete = models.SmallIntegerField(verbose_name="Время на выполнение привычки", help_text="Время указать в секундах", **NULLABLE)
    is_public = models.BooleanField(default=False, verbose_name="Видно всем")

    def __str__(self):
        return {self.move}

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
