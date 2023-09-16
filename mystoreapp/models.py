from django.db import models
from django.contrib.auth.models import User  # Import the User model if not already imported
from django.utils import timezone
# Store Model
class Store(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    owner_name = models.CharField(max_length=255,null=True)
    contact = models.CharField(max_length=255,null=True)
    purchase_data = models.CharField(max_length=255,null=True)
    description = models.TextField()
    email = models.EmailField()
    installation_time = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Task Model
class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    progress = models.PositiveIntegerField(default=0)
    task_assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_assigned_to')
    status = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

# Subtask Model
class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    field_name = models.CharField(max_length=255)
    task_feedback = models.TextField()
    field_value = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class StoreWorker(models.Model):
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} at {self.store.name}"