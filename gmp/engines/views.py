from rest_framework import viewsets

from .models import Engine, ThermClass
from .serializers import EngineSerializer, TClassSerializer

class EngineViewset(viewsets.ModelViewSet):
    queryset = Engine.objects.all()
    serializer_class = EngineSerializer

class TClassViewset(viewsets.ModelViewSet):
    queryset = ThermClass.objects.all()
    serializer_class = TClassSerializer
