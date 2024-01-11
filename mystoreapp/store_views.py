from rest_framework import generics
from .models import Store
from rest_framework.response import Response
from rest_framework import status
from .models import Store, StoreContact
from .serializers import StoreSerializer,StoreContactSerializer



class StoreCreateListView(generics.ListCreateAPIView):
    queryset = Store.objects.prefetch_related('contacts').all() 
    serializer_class = StoreSerializer

    def create(self, request, *args, **kwargs):
         serializer = self.get_serializer(data=request.data)
         if serializer.is_valid():
            store = serializer.save()  # Create Store object
            contacts_data = request.data.get('contacts')  # Get contacts data from request

            if contacts_data:
                 for contact_data in contacts_data:
                     # Create StoreContact instances associated with the created Store
                     StoreContact.objects.create(store=store, **contact_data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    
class StoreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all() 
    serializer_class = StoreSerializer


class StoreWithContactsView(generics.RetrieveAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Fetch contacts associated with the retrieved store instance
        contacts_queryset = instance.contacts.all()
        contacts_serializer = StoreContactSerializer(contacts_queryset, many=True)

        response_data = {
            'store_details': serializer.data,
            'contacts': contacts_serializer.data
        }

        return Response(response_data)