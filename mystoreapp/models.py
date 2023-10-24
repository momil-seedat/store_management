from django.db import models
from django.contrib.auth.models import User  # Import the User model if not already imported
from django.utils import timezone
# Store Model
class Store(models.Model):
    shop_name = models.CharField(max_length=255)
    sales=models.CharField(max_length=255,null=True)
    brands=models.TextField(null=True)
    address = models.TextField()
    owner_name = models.CharField(max_length=255)
    purchase_data = models.CharField(max_length=255,null=True)
    description = models.TextField()
    email = models.EmailField()
    installation_time = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contacts = models.ManyToManyField('StoreContact', related_name='store_contacts', blank=True)

    def __str__(self):
        return self.shop_name

class StoreContact(models.Model):
    store= models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store')
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

# Task Model
class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    progress = models.PositiveIntegerField(default=0)
    task_assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_assigned_to')
    status = models.CharField(max_length=50, default='BACKLOG')
    task_feedback = models.TextField(null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

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
        return f"{self.user.username} at {self.store.shop_name}"
    
class TaskSubmission(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    installation_requirements = models.TextField()
    image_1 = models.ImageField(upload_to='task_submissions/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='task_submissions/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='task_submissions/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='task_submissions/', blank=True, null=True)
    image_5 = models.ImageField(upload_to='task_submissions/', blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission for Task: {self.task.name}, User: {self.user.username}"