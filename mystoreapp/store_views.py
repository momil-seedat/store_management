from rest_framework import generics
from .models import Store
from .serializers import StoreSerializer

class StoreCreateView(generics.CreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

class StoreUpdateView(generics.UpdateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
