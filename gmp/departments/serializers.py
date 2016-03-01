from rest_framework import serializers

from .models import Measurer, Department

class DepartmentSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Department
        fields = ('name',)

class MeasurerSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = Measurer
