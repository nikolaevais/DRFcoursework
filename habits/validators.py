from datetime import timedelta
from django.utils import timezone

from django.core.exceptions import ValidationError


class FillingValidator:
    """Проверка на одновременное заполнение двух полей вознаграждение и связанная привычка."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value)
        if tmp_val.get("reward") and tmp_val.get("related_habit") is not None:
            raise ValidationError(
                'Поля "Вознаграждение" и "Связанная привычка" не могут быть заполнены одновременно. Заполните одно поле'
            )


class TimeValidator:
    """Проверка на то, что время выполнения привычки не может быть больше 2 минут."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if tmp_val is not None:
            if tmp_val > timedelta(minutes=2):
                raise ValidationError(
                    "Время на выполнение привычки не может быть больше 2 минут"
                )


class RelatedValidator:
    """Проверка, на то,что в связанные привычки могут попадать только привычки с признаком приятной привычки."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if tmp_val and not tmp_val.is_sign_of_pleasant_habit:
            print(tmp_val.is_sign_of_pleasant_habit)
            raise ValidationError("Связанная привычка должна быть приятной привычкой")


class ReValidator:
    """Проверка на то, что у приятной привычки не может быть вознаграждения или связанной привычки."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value)
        if tmp_val.get(self.field):
            if tmp_val.get("reward") or tmp_val.get("related_habit") is not None:
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки"
                )


class PeriodicityValidator:
    """Проверка на то, что нельзя выполнять привычку реже, чем 1 раз в 7 дней."""

    def __init__(self, field, field1):
        self.field = field
        self.field1 = field1

    def __call__(self, periodicity, next_reminder):
        if periodicity == 'Weekly':
            if (next_reminder - timezone.now().date()).days > 7:
                raise ValidationError("Эту привычку необходимо выполнять хотя бы раз в 7 дней.")
