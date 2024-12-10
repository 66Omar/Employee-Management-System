from rest_framework import serializers
from companies.serializers import CompanySerializer
from departments.models import Department
from companies.models import Company


class DepartmentSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    number_of_projects = serializers.IntegerField(read_only=True)
    number_of_employees = serializers.IntegerField(read_only=True)

    class Meta:
        model = Department
        fields = ["id", "name", "company", "number_of_projects", "number_of_employees"]


class CreateDepartmentSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())

    class Meta:
        model = Department
        fields = ["name", "company"]


class UpdateDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["name"]
