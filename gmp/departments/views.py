from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Department, Measurer
from .serializers import DepartmentSerializer, MeasurerSerializer

class DepartmentViewset(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class MeasurerViewset(viewsets.ViewSet):
    queryset = Measurer.objects.all()
    serializer_class = MeasurerSerializer

    def list(self, request, department_pk=None):
        department = Department.objects.get(pk=department_pk)
        measurers = self.queryset.filter(department=department)
        serializer = MeasurerSerializer(measurers , many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
