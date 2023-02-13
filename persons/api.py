from rest_framework import viewsets, permissions
from .models import Person
from .serializers import PersonSerializer

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PersonSerializer

