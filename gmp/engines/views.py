from rest_framework import viewsets

from .models import Engine
from .serializers import EngineSerializer

class EngineViewset(viewsets.ModelViewSet):
    queryset = Engine.objects.all()
    serializer_class = EngineSerializer
