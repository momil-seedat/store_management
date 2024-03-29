# Generated by Django 4.2.5 on 2023-12-09 10:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mystoreapp', '0029_assignedpermission'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignedpermission',
            name='assignee_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assignee_permissions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='assignedpermission',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_permissions', to=settings.AUTH_USER_MODEL),
        ),
    ]
