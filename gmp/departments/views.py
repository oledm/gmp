from rest_framework import viewsets

from .serializers import DepartmentSerializer, MeasurerSerializer
from .models import Department, Measurer

class DepartmentViewset(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class MeasurerViewset(viewsets.ModelViewSet):
    queryset = Measurer.objects.all()
    serializer_class = MeasurerSerializer

