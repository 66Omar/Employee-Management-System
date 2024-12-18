# Generated by Django 5.1.4 on 2024-12-08 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_is_staff_alter_user_is_superuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='company',
        ),
        migrations.RemoveField(
            model_name='emplpyee',
            name='company',
        ),
        migrations.RemoveField(
            model_name='department',
            name='company',
        ),
        migrations.RemoveField(
            model_name='project',
            name='department',
        ),
        migrations.RemoveField(
            model_name='emplpyee',
            name='department',
        ),
        migrations.RemoveField(
            model_name='emplpyee',
            name='user',
        ),
        migrations.RemoveField(
            model_name='project',
            name='assigned_employees',
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile_number',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.DeleteModel(
            name='Company',
        ),
        migrations.DeleteModel(
            name='Department',
        ),
        migrations.DeleteModel(
            name='Emplpyee',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
    ]
