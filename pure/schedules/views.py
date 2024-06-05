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
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filter_parameters = {"class": "_class__name"}
    filter_backends = [TodayFilterBackend]
