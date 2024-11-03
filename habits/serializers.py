from rest_framework import serializers

from habits.models import Habits
from habits.validators import (
    FillingValidator,
    TimeValidator,
    RelatedValidator,
    ReValidator, PeriodicityValidator,
)


class HabitsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habits
        fields = "__all__"
        validators = [
            (FillingValidator("move")),
            (TimeValidator("time_to_complete")),
            (RelatedValidator("related_habit")),
            (ReValidator("is_sign_of_pleasant_habit")),
            (PeriodicityValidator("periodicity", "next_reminde"))
        ]
