from rest_framework import viewsets

from .models import Organization, LPU
from .serializers import OrganizationSerializer, LPUSerializer

class OrganizationViewset(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class LPUViewset(viewsets.ModelViewSet):
    queryset = LPU.objects.all()
    serializer_class = LPUSerializer
