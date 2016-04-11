from rest_framework import viewsets
from .models import Container
from .serializers import ContainerSerializer

# Create your views here.
class ContainerViewset(viewsets.ModelViewSet):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
