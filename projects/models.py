from django.db import models


class Project(models.Model):
    company = models.ForeignKey(
        "companies.Company", related_name="projects", on_delete=models.CASCADE
    )
    department = models.ForeignKey(
        "departments.Department", related_name="projects", on_delete=models.CASCADE
    )
    project_name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    assigned_employees = models.ManyToManyField("employees.Employee")
