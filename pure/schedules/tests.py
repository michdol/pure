from datetime import datetime

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from unittest import mock

from schedules.models import Schedule


class ScheduleViewSetTest(TestCase):
    fixtures = [
        "schedules/fixtures/classes.yaml",
        "schedules/fixtures/schedules.yaml",
        "schedules/fixtures/students.yaml",
        "schedules/fixtures/subjects.yaml",
        "schedules/fixtures/teachers.yaml",
    ]

    def setUp(self):
        super().setUp()
        self.client = APIClient()

    def test_get(self):
        response = self.client.get("/schedules/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_count = Schedule.objects.all().count()
        self.assertEqual(expected_count, len(response.data))

        schedule1 = response.data[0]
        schedule2 = response.data[1]
        schedule1_hour = datetime.strptime(schedule1["hour"], "%H:%M:%S").time()
        schedule2_hour = datetime.strptime(schedule2["hour"], "%H:%M:%S").time()
        self.assertLess(schedule1_hour, schedule2_hour)

    def test_get_by_class_name(self):
        class_param = "5A"
        response = self.client.get("/schedules/", data={"class": class_param})
        expected_count = Schedule.objects.filter(_class__name=class_param).count()
        self.assertEqual(len(response.data), expected_count)

    @mock.patch("schedules.filters.datetime")
    def test_get_by_class_name_today(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 6, 5, 3, 10, 0, 0)
        class_param = "5A"
        response = self.client.get("/schedules/", data={"class": class_param, "today": True})
        expected_count = Schedule.objects.filter(_class__name=class_param, day_of_week=1).count()
        self.assertEqual(len(response.data), expected_count)
