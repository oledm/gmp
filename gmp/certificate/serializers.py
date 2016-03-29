from rest_framework import serializers
from .models import Certificate, ControlType


class ControlTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlType
        fields = ('name', 'full_name')


class CertificateSerializer(serializers.ModelSerializer):
    control_types = ControlTypeSerializer(many=True)

    class Meta:
        model = Certificate
