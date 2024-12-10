from employees.models import Employee


def IsAdmin(user_id, company_id) -> bool:
    return Employee.objects.filter(
        user_id=user_id,
        company_id=company_id,
        role=Employee.ADMIN,
        employee_status=Employee.HIRED,
    ).exists()


def IsAdminOrManager(user_id, company_id) -> bool:
    return Employee.objects.filter(
        user_id=user_id,
        company_id=company_id,
        role__in=[Employee.ADMIN, Employee.MANAGER],
        employee_status=Employee.HIRED,
    ).exists()


def IsEmployee(user_id, company_id) -> bool:
    return Employee.objects.filter(
        user_id=user_id,
        company_id=company_id,
        role__in=[Employee.ADMIN, Employee.MANAGER, Employee.EMPLOYEE],
        employee_status=Employee.HIRED,
    ).exists()
