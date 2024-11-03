from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from habits.models import Habits
from users.services import send_telegram_message


@shared_task
def send_telegram():
    """отправка в телеграмм напоминания о привычке"""
    now = timezone.now()
    print(f"дата {now}")
    habits = Habits.objects.filter(
        next_reminde=now.date(), times__hour=now.hour, times__minute=now.minute
    )
    for habit in habits:
        print(habit)
        message = f"Сейчас необходимо {habit.move} в {habit.location} за {habit.time_to_complete} минут."
        if habit.user.tg_chat_id:
            send_telegram_message(habit.user.tg_chat_id, message)
            if habit.periodicity == "EVERYDAY":
                habit.next_reminde += timedelta(days=1)
            elif habit.periodicity == "EVERYWEEK":
                habit.next_reminde += timedelta(days=2)
            elif habit.periodicity == "EVERYWEEK":
                habit.next_reminde += timedelta(days=3)
            elif habit.periodicity == "EVERYWEEK":
                habit.next_reminde += timedelta(days=4)
            elif habit.periodicity == "EVERYWEEK":
                habit.next_reminde += timedelta(days=5)
            elif habit.periodicity == "EVERYWEEK":
                habit.next_reminde += timedelta(days=6)
            elif habit.periodicity == "EVERYWEEK":
                habit.next_reminde += timedelta(days=7)
            habit.save()
