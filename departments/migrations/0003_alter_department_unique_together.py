# Generated by Django 5.1.4 on 2024-12-09 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_alter_company_name'),
        ('departments', '0002_alter_department_company'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='department',
            unique_together={('name', 'company')},
        ),
    ]
