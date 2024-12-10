from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Department


@receiver(pre_save, sender=Department)
def modify_department_name(sender, instance, **kwargs):
    if not instance.pk:
        instance.name = f"{instance.company.name} - {instance.name}"
