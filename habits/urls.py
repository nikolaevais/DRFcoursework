from django.urls import path
from rest_framework.permissions import AllowAny

from rest_framework.routers import DefaultRouter

from habits.apps import HabitsConfig
from habits.views import HabitsViewSet, HabitsPublicListAPIView

app_name = HabitsConfig.name


router = DefaultRouter()
router.register(r"habits", HabitsViewSet, basename="habits")

urlpatterns = [
    path(
        "public/",
        HabitsPublicListAPIView.as_view(permission_classes=(AllowAny,)),
        name="habits_public",
    ),
] + router.urls
