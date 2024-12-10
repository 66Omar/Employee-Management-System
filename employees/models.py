from django.db import models
from django.utils import timezone


class Employee(models.Model):
    APPLICATION_RECEIVED = "application_received"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    HIRED = "hired"
    NOT_ACCEPTED = "not_accepted"

    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"

    STATUS_CHOICES = [
        (APPLICATION_RECEIVED, "Application Received"),
        (INTERVIEW_SCHEDULED, "Interview Scheduled"),
        (HIRED, "Hired"),
        (NOT_ACCEPTED, "Not Accepted"),
    ]

    ROLE_CHOICES = [
        (ADMIN, "Admin"),
        (MANAGER, "Manager"),
        (EMPLOYEE, "Employee"),
    ]

    user = models.ForeignKey(
        "users.User", related_name="employments", on_delete=models.CASCADE
    )
    company = models.ForeignKey(
        "companies.Company", related_name="employees", on_delete=models.CASCADE
    )
    department = models.ForeignKey(
        "departments.Department", related_name="employees", on_delete=models.CASCADE
    )
    employee_status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default=APPLICATION_RECEIVED
    )
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default=EMPLOYEE)
    designation = models.CharField(max_length=100)
    hired_on = models.DateTimeField(null=True, blank=True)

    def can_transition_to(self, target_status):
        valid_transitions = {
            self.APPLICATION_RECEIVED: [self.INTERVIEW_SCHEDULED, self.NOT_ACCEPTED],
            self.INTERVIEW_SCHEDULED: [self.HIRED, self.NOT_ACCEPTED],
            self.NOT_ACCEPTED: [self.INTERVIEW_SCHEDULED],
        }
        return target_status in valid_transitions.get(self.employee_status, [])

    def transition_to(self, target_status):
        if not self.can_transition_to(target_status):
            raise ValueError(
                f"Invalid transition from {self.employee_status} to {target_status}."
            )
        self.employee_status = target_status
        if target_status == self.HIRED:
            self.hired_on = timezone.now()
        self.save()

    class Meta:
        unique_together = ("user", "company")
