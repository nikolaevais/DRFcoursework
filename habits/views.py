from rest_framework import viewsets
from rest_framework.generics import ListAPIView

from habits.models import Habits
from habits.paginators import CustomPagination
from habits.serializers import HabitsSerializer
from users.permissions import IsOwmer


class HabitsViewSet(viewsets.ModelViewSet):
    """ViewSet for habits"""

    serializer_class = HabitsSerializer
    queryset = Habits.objects.all()
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        habits = serializer.save()
        habits.user = self.request.user
        habits.save()

    def get_permissions(self):
        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            self.permission_classes = (IsOwmer,)
        return super().get_permissions()


class HabitsPublicListAPIView(ListAPIView):
    """вывод всех публичных привычек"""

    queryset = Habits.objects.filter(is_public=True).order_by("pk")
    serializer_class = HabitsSerializer
