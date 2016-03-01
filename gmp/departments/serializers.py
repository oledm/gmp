from rest_framework import serializers

from .models import Instrument, Department

class DepartmentSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Department
        fields = ('name',)

class InstrumentSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = Instrument
