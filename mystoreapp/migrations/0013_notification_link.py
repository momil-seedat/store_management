# Generated by Django 4.2.5 on 2023-11-11 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mystoreapp', '0012_city_notification_district'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='link',
            field=models.TextField(null=True),
        ),
    ]
