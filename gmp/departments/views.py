from rest_framework import viewsets

from .models import Department, Measurer
from .serializers import DepartmentSerializer, MeasurerSerializer

class DepartmentViewset(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class MeasurerViewset(viewsets.ModelViewSet):
    queryset = Measurer.objects.all()
    serializer_class = MeasurerSerializer

