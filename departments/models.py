from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(
        "companies.Company", related_name="departments", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ["name", "company"]
