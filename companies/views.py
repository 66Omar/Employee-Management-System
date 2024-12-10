from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from employees.models import Employee
from departments.models import Department
from .serializers import *
from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404
from employees.utils import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Count
from departments.serializers import DepartmentSerializer
from employees.serializers import EmployeeSerializer
from rest_framework.decorators import api_view
from django.db.models import Prefetch


class CompanyAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @staticmethod
    def get_queryset():
        """
        Queryset to get companies annotated with num of departments, projects and employees
        """
        return Company.objects.annotate(
            number_of_departments=Count("departments", distinct=True),
            number_of_projects=Count("projects", distinct=True),
            number_of_employees=Count("employees", distinct=True),
        )

    def get(self, request, company_id=None):
        """
        [PUBLIC]
        Get all companies
        """
        if company_id:
            return self.get_company_by_id(request, company_id)
        companies = self.get_queryset().all()
        serialized_companies = CompanySerializer(companies, many=True)
        return Response(serialized_companies.data, status.HTTP_200_OK)

    def get_company_by_id(self, request, company_id):
        """
        [PUBLIC]
        Get company by ID
        """
        company = get_object_or_404(
            self.get_queryset(),
            id=company_id,
        )
        serialized_company = CompanySerializer(company)
        return Response(serialized_company.data, status.HTTP_200_OK)

    def post(self, request):
        """
        [PUBLIC]
        Creates a company object, and automatically creates an employee for the admin
        as well as a default department with name {{company_name}} - Main this is
        all done through a transaction
        """
        try:
            with transaction.atomic():
                company_serializer = CompanySerializer(data=request.data)
                if not company_serializer.is_valid():
                    return Response(
                        company_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
                company = company_serializer.save()

                department = Department.objects.create(
                    company=company,
                    name="Main",
                )

                Employee.objects.create(
                    user=request.user,
                    company=company,
                    department=department,
                    designation="CEO",
                    role=Employee.ADMIN,
                    employee_status=Employee.HIRED,
                    hired_on=timezone.now(),
                )

                return Response(company_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, company_id):
        """
        [PRIVATE] admins only
        Update company by ID
        """
        if not IsAdmin(request.user, company_id):
            return Response({"detail": "Unauthorized Employee"}, 401)
        company = get_object_or_404(Company, id=company_id)

        company_serializer = CompanySerializer(company, data=request.data, partial=True)
        if not company_serializer.is_valid():
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        company_serializer.save()
        return Response(company_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, company_id):
        """
        [PRIVATE] admins only
        Delete a company by ID
        """
        if not IsAdmin(request.user, company_id):
            return Response({"detail": "Unauthorized Employee"}, 401)

        company = get_object_or_404(Company, id=company_id)
        serialized_company = CompanySerializer(company).data
        company.delete()
        return Response(serialized_company, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_company_departments(request, company_id):
    company = get_object_or_404(
        Company.objects.prefetch_related(
            Prefetch(
                "departments",
                queryset=Department.objects.annotate(
                    number_of_employees=Count("employees", distinct=True),
                    number_of_projects=Count("projects", distinct=True),
                ),
            )
        ),
        id=company_id,
    )
    serialized_deparments = DepartmentSerializer(company.departments, many=True).data
    return Response(serialized_deparments, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_company_employees(request, company_id):
    company = get_object_or_404(
        Company.objects.prefetch_related(
            Prefetch(
                "employees",
                queryset=Employee.objects.select_related(
                    "department", "company", "user"
                ),
            )
        ),
        id=company_id,
    )
    serialized_employees = EmployeeSerializer(company.employees, many=True).data
    return Response(serialized_employees, status=status.HTTP_200_OK)
