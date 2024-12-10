from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from employees.models import Employee
from .serializers import *
from django.shortcuts import get_object_or_404
from employees.utils import *
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Count


class EmployeeAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @staticmethod
    def get_queryset():
        return Employee.objects.select_related(
            "user", "company", "department"
        ).annotate(
            number_of_assigned_projects=Count("project", distinct=True),
        )

    def get(self, request, employee_id=None):
        """
        [PUBLIC]
        Retrieves all employees, employee_id is provided, it will only get data for only that employee
        """
        if employee_id:
            return self.get_employee_by_id(request, employee_id)
        employees = self.get_queryset().all()
        serialized_employees = EmployeeSerializer(employees, many=True).data
        return Response(serialized_employees, status=status.HTTP_200_OK)

    def get_employee_by_id(self, request, employee_id):
        """
        [PUBLIC]
        Retrieves employee by ID
        """
        employee = get_object_or_404(self.get_queryset(), id=employee_id)
        serialized_employee = EmployeeSerializer(employee).data
        return Response(serialized_employee, status=status.HTTP_200_OK)

    def post(self, request):
        """
        [PUBLIC]
        If an admin or a manager of a company is sending a request, it will act as an invitation (method below)
        else it will be as the employee is applying for the job, their application status will be "application_received"
        """
        if IsAdminOrManager(request.user.id, request.data.get("company")):
            return self.invite_employee(request)

        if request.user.id != request.data.get("user"):
            return Response(
                {"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
        request.data["employee_status"] = Employee.APPLICATION_RECEIVED

        employee_serializer = CreateEmployeeSerializer(data=request.data)
        if not employee_serializer.is_valid():
            return Response(
                employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        employee_serializer.save()
        return Response(employee_serializer.data, 200)

    def invite_employee(self, request):
        """
        [PRIVATE]
        Admin or manager invited a user to their company, their employment status will automatically be "interview_scheduled"
        """
        request.data["employee_status"] = Employee.INTERVIEW_SCHEDULED
        employee_serializer = CreateEmployeeSerializer(data=request.data)
        if not employee_serializer.is_valid():
            return Response(
                employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        employee_serializer.save()
        return Response(employee_serializer.data, 200)

    def patch(self, request, employee_id):
        """
        [PRIVATE] admins and managers
        Update employee by ID
        """
        employee = get_object_or_404(Employee, id=employee_id)
        if not IsAdminOrManager(request.user.id, employee.company_id):
            return Response(
                {"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
        employee_serializer = UpdateEmployeeSerializer(
            employee, data=request.data, partial=True
        )
        if not employee_serializer.is_valid():
            return Response(
                employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        employee_serializer.save()
        return Response(employee_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, employee_id):
        """
        [PRIVATE] admins only
        delete employee by ID
        """
        employee = get_object_or_404(Employee, id=employee_id)

        if not IsAdmin(request.user.id, employee.id):
            return Response(
                {"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

        serialized_employee = EmployeeSerializer(employee).data
        employee.delete()
        return Response(serialized_employee, status=status.HTTP_200_OK)


class EmployeeStatusTransitionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, employee_id):
        """
        [PRIVATE] admins and managers
        Get employee status by employee ID, returns current status and possible transitions for that employee
        """
        employee = get_object_or_404(Employee, id=employee_id)

        if not IsAdminOrManager(request.user.id, employee.company_id):
            return Response(
                {"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            {
                "current_status": employee.employee_status,
                "possible_transitions": [
                    transition[0]
                    for transition in Employee.STATUS_CHOICES
                    if employee.can_transition_to(transition[0])
                ],
            }
        )

    def post(self, request, employee_id):
        """
        [PRIVATE] admins and managers
        Update application status for that employee, while this can be done on employee update,
        this goes through the onboarding process step by step, and you can't skip any steps
        """
        employee = get_object_or_404(Employee, id=employee_id)
        target_status = request.data.get("status")

        if not IsAdminOrManager(request.user.id, employee.company_id):
            return Response(
                {"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            employee.transition_to(target_status)
            return Response({"status": employee.employee_status})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
