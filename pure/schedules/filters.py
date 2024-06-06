from datetime import datetime
from rest_framework import filters


class TodayFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.query_params.get("today"):
            today_weekday = datetime.now().weekday()
            queryset = queryset.filter(day_of_week=today_weekday)
        return queryset
