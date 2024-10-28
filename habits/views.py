from rest_framework import viewsets

from habits.models import Habits
from habits.paginators import CustomPagination
from habits.serializers import HabitsSerializer


class HabitsViewSet(viewsets.ModelViewSet):
    serializer_class = HabitsSerializer
    queryset = Habits.objects.all()
    pagination_class = CustomPagination