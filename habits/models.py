from django.db import models

from config import settings
from users.models import NULLABLE


class Habits(models.Model):
    EV = "Everyday"
    OETD = "Once every two days"
    OEThD = "Once every three days"
    OEFD = "Once every four days"
    OEFiD = "Once every five days"
    OESD = "Once every six days"
    W = "Weekly"

    PERIOD_DAY = [
        (EV, "каждый день"),
        (OETD, "раз в два дня"),
        (OEThD, "раз в три дня"),
        (OEFD, "раз в четыре дня"),
        (OEFiD, "раз в пять дней"),
        (OESD, "раз в шесть дней"),
        (W, "раз в неделю"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Создатель привычки",
        **NULLABLE
    )
    location = models.CharField(max_length=250, verbose_name="Место")
    times = models.TimeField(verbose_name="Время, когда необходимо выполнить привычку")
    move = models.CharField(max_length=250, verbose_name="Действие")
    is_sign_of_pleasant_habit = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки"
    )
    related_habit = models.ForeignKey(
        "self", on_delete=models.CASCADE, verbose_name="Связанная привычка", **NULLABLE
    )
    periodicity = models.CharField(
        max_length=50,
        default="EVERYDAY",
        verbose_name="Периодичность",
        choices=PERIOD_DAY,
    )
    reward = models.CharField(max_length=250, verbose_name="Вознаграждение", **NULLABLE)
    time_to_complete = models.DurationField(
        verbose_name="Время на выполнение привычки", **NULLABLE
    )
    is_public = models.BooleanField(default=False, verbose_name="Видно всем")
    next_reminde = models.DateField(
        auto_now_add=True,
        verbose_name="Время, когда необходимо выполнить следующий раз привычку",
        **NULLABLE
    )

    def __str__(self):
        return self.move

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
