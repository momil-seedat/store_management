# views.py

from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User, Group
from .models import UserAttribute
from .serializers import UserSerializer, GroupSerializer, UserCreationSerializer
from django.contrib.auth.hashers import make_password

class UsersByGroupView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        group_name = self.kwargs['group_name']  # Get the group name from the URL parameter
        return User.objects.filter(groups__name=group_name, is_active=True)

class AllUsersView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(is_active=True) 
    
class GroupViews(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class CreateUserWithAttributes(APIView):
    def post(self, request, format=None):
        user_data = request.data.copy() 
        password = request.data.get('password')
        hashed_password = make_password(password)
        user_data['password'] = hashed_password
        user_serializer = UserCreationSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()

            group_id = request.data.get('user_group')
            if group_id:
                group = Group.objects.get(pk=group_id)
                user.groups.add(group)

            district_id = request.data.get('district')
            mobile_no = request.data.get('mobile_no')

            UserAttribute.objects.create(user=user, district_id=district_id, mobile_no=mobile_no)

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)