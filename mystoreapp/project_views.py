# views.py
from rest_framework import generics
from .models import Project
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .serializers import ProjectSerializer , AddProjectSerializer
import json
from .signals import generate_project_serial_number


class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = AddProjectSerializer

    def get_serializer_class(self):
        # Use different serializer for list view
        if self.request.method == 'GET':
            return ProjectSerializer  # Change ListProjectSerializer to your actual serializer class
        else:
            return AddProjectSerializer

    def perform_create(self, serializer):
        # Generate a random serial number for the project
       # project_serial = generate_project_serial_number()
        
        # Add the generated serial numbers to the serializer data before saving
        serializer.save()


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer



@csrf_exempt
def projects_by_created_by(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            created_by_id = data.get('created_by')

            if created_by_id is not None:
                created_by_user = User.objects.filter(id=created_by_id).first()
                if created_by_user:
                    projects = Project.objects.filter(created_by=created_by_user)
                    projects_data = []
                    for project in projects:
                        store_info = None
                        if project.store:
                            store_info = {
                                'store_id': project.store.id,
                                'shop_name': project.store.shop_name,
                            }

                        projects_data.append({
                            'id': project.id,
                            'title': project.title,
                            'description': project.description,
                            'project_serial_no': project.project_serial_no,
                            'store_info': store_info,
                            'created_at': project.created_at.strftime('%d-%m-%Y'),
                            'updated_at': project.updated_at.strftime('%d-%m-%Y'),
                        })

                    return JsonResponse({'projects': projects_data}, safe=False)
                else:
                    return JsonResponse({'error': 'User not found'}, status=404)
            else:
                return JsonResponse({'error': 'Parameter created_by is required'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
@csrf_exempt
def projects_by_store(request, store_id):
    try:
        if request.method == 'GET':
            # Fetch projects related to the provided store ID
            projects = Project.objects.filter(store_id=store_id)

            # Serialize projects data
            serialized_projects = list(projects.values('id', 'title','project_serial_no','description'))  # Assuming 'id' and 'name' are fields in the Project model

            return JsonResponse({'projects': serialized_projects}, safe=False)
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)