from django.contrib import admin
from habits.models import Habits


@admin.register(Habits)
class Habits(admin.ModelAdmin):
    list_display = ('user', 'location', 'times', 'move', 'is_sign_of_pleasant_habit', 'related_habit', 'periodicity', 'reward', 'time_to_complete', 'is_public')