from rest_framework import serializers

from .models import Measurer, Department
from gmp.reports.serializers import ReportSerializer

class DepartmentSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    report_types = ReportSerializer(many=True, required=False)

    class Meta:
        model = Department

class MeasurerSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = Measurer
