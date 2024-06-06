from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets

from schedules.filters import TodayFilterBackend
from schedules.models import Schedule
from schedules.serializers import ScheduleSerializer


class FilterByParamMixin():
    filter_parameters = {}

    def get_queryset(self):
        queryset = super().get_queryset()
        query_aruments = {}

        for param, lookup in self.filter_parameters.items():
            value = self.request.query_params.get(param)
            if value:
                query_aruments[lookup] = value

        if query_aruments:
            queryset = queryset.filter(**query_aruments)
        return queryset


class ScheduleViewSet(FilterByParamMixin, viewsets.ModelViewSet):
    queryset = Schedule.objects.all().prefetch_related("_class", "_class__students", "subject", "subject__teacher")
    serializer_class = ScheduleSerializer
    filter_parameters = {"class": "_class__name"}
    filter_backends = [TodayFilterBackend]

    @method_decorator(cache_page(60))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)
