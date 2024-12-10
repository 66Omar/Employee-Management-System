from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from departments.models import Department
from .serializers import *
from django.shortcuts import get_object_or_404
from employees.utils import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Count, Prefetch
from rest_framework.decorators import api_view
from employees.serializers import EmployeeSerializer


class DepartmentAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @staticmethod
    def get_annotated_queryset():
        return Department.objects.select_related("company").annotate(
            number_of_employees=Count("employees", distinct=True),
            number_of_projects=Count("projects", distinct=True),
        )

    def get(self, request, department_id=None):
        if department_id:
            return self.get_department_by_id(request, department_id)
        departments = self.get_annotated_queryset().all()
        serialized_departments = DepartmentSerializer(departments, many=True).data
        return Response(serialized_departments, status=status.HTTP_200_OK)

    def get_department_by_id(self, request, department_id):
        department = get_object_or_404(self.get_annotated_queryset(), id=department_id)
        serialized_department = DepartmentSerializer(department).data
        return Response(serialized_department, status=status.HTTP_200_OK)

    def post(self, request):
        department_serializer = CreateDepartmentSerializer(data=request.data)

        if not IsAdminOrManager(request.user.id, request.data.get("company")):
            return Response(
                {"detail": "Unauthorized Employee"}, status=status.HTTP_401_UNAUTHORIZED
            )

        if not department_serializer.is_valid():
            return Response(
                department_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        department_serializer.save()
        return Response(department_serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, department_id):
        department = get_object_or_404(Department, id=department_id)
        department_serializer = UpdateDepartmentSerializer(
            department, data=request.data, partial=True
        )

        if not IsAdminOrManager(request.user.id, department.company_id):
            return Response(
                {"detail": "Unauthorized Employee"}, status=status.HTTP_401_UNAUTHORIZED
            )

        if not department_serializer.is_valid():
            return Response(
                department_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        department_serializer.save()
        return Response(department_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, department_id):

        department = get_object_or_404(Department, id=department_id)
        serialized_department = DepartmentSerializer(department).data
        if not IsAdmin(request.user.id, department.company_id):
            return Response(
                {"detail": "Unauthorized Employee"}, status=status.HTTP_401_UNAUTHORIZED
            )

        department.delete()
        return Response(serialized_department, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_department_employees(request, department_id):
    department = get_object_or_404(
        Department.objects.prefetch_related(
            Prefetch(
                "employees",
                queryset=Employee.objects.select_related(
                    "department", "company", "user"
                ),
            )
        ),
        id=department_id,
    )
    serialized_employees = EmployeeSerializer(department.employees, many=True).data
    return Response(serialized_employees, status=status.HTTP_200_OK)
