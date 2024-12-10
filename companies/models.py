from django.db import models


class Company(models.Model):
    name = models.CharField(unique=True, max_length=255)