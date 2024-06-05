from rest_framework import serializers

from schedules.models import Class, Schedule, Subject, Teacher


class ClassSerializer(serializers.ModelSerializer):
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = ["name", "student_count"]

    def get_student_count(self, instance):
        return instance.students.count()


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["name"]


class ScheduleSerializer(serializers.ModelSerializer):
    _class = ClassSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    teacher = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = ["_class", "subject", "day_of_week", "hour", "teacher"]

    def get_teacher(self, instance):
        return {"name": instance.subject.teacher.name}

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["class"] = ret.pop("_class")
        return ret
