# Generated by Django 4.2.5 on 2024-01-22 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mystoreapp', '0035_remove_userattribute_city_userattribute_district'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='channel',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='grade',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
