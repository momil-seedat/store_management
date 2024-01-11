from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics
from .serializers import AssignedPermissionSerializer,AddPermissionsSerializer
from .models import AssignedPermission, Project
import json


class AssignedPermissionListView(generics.ListCreateAPIView):
    queryset = AssignedPermission.objects.all()
    serializer_class = AddPermissionsSerializer

class AssignedPermissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AssignedPermission.objects.all()
    serializer_class = AssignedPermission

@csrf_exempt
def fetch_assigned_projects(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')

        if user_id:
            user = User.objects.filter(id=user_id).first()
            if user:
              
                assigned_permissions = AssignedPermission.objects.filter(user_id=user)
                assigned_projects = [permission.project_id for permission in assigned_permissions]
                projects = Project.objects.filter( Q(id__in=assigned_projects) | Q(created_by=user)).order_by('-created_at')

        # Sorting by created_at (ascending order)
                

                projects_data = []
                for project in projects:
                    projects_data.append({
                        'project_id': project.id,
                        'title': project.title,
                        'description': project.description,
                        'project_serial_no': project.project_serial_no,
                        'created_at':  project.created_at.strftime('%d-%m-%Y'),
                        'store':project.store.shop_name,
                        'created_by': project.created_by.username

                        # Include other project details as needed
                    })
                return JsonResponse({'assigned_projects': projects_data}, safe=False)
            else:
                  return JsonResponse({'error': 'Invalid user'}, status=400)
            
        else:
            return JsonResponse({'error': 'Parameter user_id is required'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
