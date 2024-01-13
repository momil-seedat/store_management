from rest_framework import generics, status
from .models import Task
from .serializers import TaskSerializer, AddTaskSerializer,TaskObjectSerializer
from .models import Project, Notification
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
from .signals import generate_task_serial_number

class TaskCreateListView(generics.ListCreateAPIView):
    queryset = Task.objects.all().order_by('-start_date')
    serializer_class = AddTaskSerializer

    def perform_create(self, serializer):
        project_id = self.request.data.get('project')  # Assuming project ID is sent in the request data
        project_serial = None

        if project_id:
            try:
                project = Project.objects.get(id=project_id)
                project_serial = project.project_serial_no
            except Project.DoesNotExist:
                pass

        task_serial = None
        if project_serial:
            task_serial = generate_task_serial_number(project_serial)

        task=serializer.save(task_serial_no=task_serial)
        notification_text = f"A new task has been created: {task.name}"
        notification_link = f"/task-mangement/task_profile/{task.id}"  # Change this to the appropriate link for your task details
        Notification.objects.create(text=notification_text, link=notification_link, user_id=task.task_assigned_to,type="Task Added")


    def get_serializer_class(self):
        # Use different serializer for list view
        if self.request.method == 'GET':
            return TaskObjectSerializer  # Change ListProjectSerializer to your actual serializer class
        else:
            return AddTaskSerializer    

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

@csrf_exempt
def fetch_tasks(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        assignee_id = data.get('assignee')
        assigned_to_id = data.get('assigned_to')
        project_id = data.get('project_id')

        user_id = None
        filter_param = None

        if assignee_id:
            user_id = assignee_id
            filter_param = 'assignee'
        elif project_id:
            tasks = Task.objects.filter(project_id=project_id)
        elif assigned_to_id:
            user_id = assigned_to_id
            filter_param = 'task_assigned_to'

        if filter_param:
            user = User.objects.filter(id=user_id).first()
            if user:
                tasks = Task.objects.filter(**{filter_param: user})
            else:
                return JsonResponse({'error': 'User not found'}, status=404)

        tasks_data = []
        for task in tasks:
            project_serial_no = task.project.project_serial_no if task.project else None
            assigned_by = task.project.created_by.username if task.project else None

            tasks_data.append({
                'task_id': task.id,
                'status': task.status,
                'task_serial': task.task_serial_no,
                'project_serial_no': project_serial_no,
                'assigned_to': task.task_assigned_to.username,
                'assignee': task.assignee.username,
                'created_at': task.start_date.strftime('%d-%m-%Y'),
            })

        return JsonResponse({'tasks': tasks_data}, safe=False)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def update_task(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task does not exist"}, status=404)

    if request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)

        new_status = data.get('status')
        new_feedback = data.get('task_feedback')
        
        if new_status:
            task.status = new_status
        if new_feedback:
            task.task_feedback = new_feedback

        task.save()

        # Create a notification for the assigned user
        notification_text = f"Task {task_id} status/feedback updated: {task.status} - {task.task_feedback}"
        Notification.objects.create(
            text=notification_text,
            type="Task Update",
            user_id=task.task_assigned_to,
        )

        serializer = TaskSerializer(task)
        response_data = {
            "message": "Task status and feedback updated successfully",
            "code":"000"
           
        }

        return JsonResponse(response_data, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=400)