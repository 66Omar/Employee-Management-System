from rest_framework import serializers
from .models import Employee
from companies.serializers import CompanySerializer
from departments.serializers import DepartmentSerializer
from users.serializers import UserSerializer
from django.utils import timezone


class EmployeeSerializer(serializers.ModelSerializer):
    number_of_assigned_projects = serializers.IntegerField(read_only=True)
    company = CompanySerializer(read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    mobile_number = serializers.CharField(source="user.mobile_number", read_only=True)
    address = serializers.EmailField(source="user.address", read_only=True)
    days_employed = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            "id",
            "username",
            "email",
            "mobile_number",
            "address",
            "company",
            "department",
            "employee_status",
            "hired_on",
            "number_of_assigned_projects",
            "days_employed",
        ]
        depth = 1

    def get_days_employed(self, obj):
        if not obj.hired_on:
            return 0
        return (timezone.now().date() - obj.hired_on.date()).days


class CreateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["user", "company", "department", "designation", "employee_status"]

    def validate(self, data):

        if data["department"].company != data["company"]:
            raise serializers.ValidationError(
                "Department does not belong to the selected company."
            )
        return data


class UpdateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["department", "designation", "employee_status"]

    def validate(self, data):
        company = self.instance.company
        if data["department"].company != company:
            raise serializers.ValidationError(
                "Department does not belong to the selected company."
            )
        return data
