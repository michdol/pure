from django.db import models

from schedules.constants import DAY_OF_WEEK


class Schedule(models.Model):
    _class = models.ForeignKey("Class", on_delete=models.CASCADE)
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=tuple(sorted(DAY_OF_WEEK.items())))
    hour = models.TimeField()


class Class(models.Model):
    name = models.CharField(max_length=256)


class Student(models.Model):
    name = models.CharField(max_length=256)
    _class = models.ForeignKey("Class", on_delete=models.CASCADE, related_name="students")


class Subject(models.Model):
    name = models.CharField(max_length=256)
    teacher = models.ForeignKey("Teacher", null=True, blank=True, on_delete=models.SET_NULL, related_name="subjects")


class Teacher(models.Model):
    name = models.CharField(max_length=256)
