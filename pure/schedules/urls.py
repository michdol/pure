from django.urls import include, path
from rest_framework import routers

from schedules.views import ScheduleViewSet

router = routers.DefaultRouter()
router.register(r"", ScheduleViewSet, basename="schedule_list")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
]