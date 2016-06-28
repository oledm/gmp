from rest_framework import viewsets

from .models import Engine, ThermClass, Connection
from .serializers import EngineSerializer, TClassSerializer, ConnectionTypesSerializer

class EngineViewset(viewsets.ModelViewSet):
    queryset = Engine.objects.all()
    serializer_class = EngineSerializer

class TClassViewset(viewsets.ModelViewSet):
    queryset = ThermClass.objects.all()
    serializer_class = TClassSerializer

class ConnectionTypesViewset(viewsets.ModelViewSet):
    queryset = Connection.objects.all()
    serializer_class = ConnectionTypesSerializer
