from rest_framework import viewsets, generics

from .serializers import DepartmentSerializer, InstrumentSerializer
from .models import Department, Instrument

class DepartmentList(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

