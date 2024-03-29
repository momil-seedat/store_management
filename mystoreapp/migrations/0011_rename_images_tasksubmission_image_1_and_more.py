# Generated by Django 4.2.5 on 2023-09-23 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mystoreapp', '0010_alter_storecontact_store'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tasksubmission',
            old_name='images',
            new_name='image_1',
        ),
        migrations.RenameField(
            model_name='tasksubmission',
            old_name='text_info',
            new_name='installation_requirements',
        ),
        migrations.AddField(
            model_name='task',
            name='task_feedback',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='tasksubmission',
            name='image_2',
            field=models.ImageField(blank=True, null=True, upload_to='task_submissions/'),
        ),
        migrations.AddField(
            model_name='tasksubmission',
            name='image_3',
            field=models.ImageField(blank=True, null=True, upload_to='task_submissions/'),
        ),
        migrations.AddField(
            model_name='tasksubmission',
            name='image_4',
            field=models.ImageField(blank=True, null=True, upload_to='task_submissions/'),
        ),
        migrations.AddField(
            model_name='tasksubmission',
            name='image_5',
            field=models.ImageField(blank=True, null=True, upload_to='task_submissions/'),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(default='BACKLOG', max_length=50),
        ),
    ]
