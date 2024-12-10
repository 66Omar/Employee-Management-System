from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        depth = 1


class CreateProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = [
            "company",
            "department",
            "project_name",
            "start_date",
            "end_date",
            "assigned_employees",
        ]

    def validate(self, data):
        company = data.get("company")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        assigned_employees = data.get("assigned_employees", [])

        if data["department"].company != company:
            raise serializers.ValidationError(
                "Department does not belong to the selected company."
            )

        if start_date and end_date and end_date <= start_date:
            raise serializers.ValidationError("End date must be after the start date.")

        for employee in assigned_employees:
            if employee.company_id != company.id:
                raise serializers.ValidationError(
                    f"Employee {employee.id} does not belong to the selected company."
                )
        return data


class UpdateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "department",
            "project_name",
            "start_date",
            "end_date",
            "assigned_employees",
        ]

    def validate(self, data):
        company = self.instance.company
        assigned_employees = data.get("assigned_employees", [])
        start_date = data.get("start_date") or self.instance.start_date
        end_date = data.get("end_date") or self.instance.end_date

        if data.get("department") and data["department"].company != company:
            raise serializers.ValidationError(
                "Department does not belong to the selected company."
            )

        if start_date and end_date and end_date <= start_date:
            raise serializers.ValidationError("End date must be after the start date.")

        for employee in assigned_employees:
            if employee.company_id != company.id:
                raise serializers.ValidationError(
                    f"Employee {employee.id} does not belong to the selected company."
                )
        return data
