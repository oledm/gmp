from rest_framework import serializers

from .models import Organization, LPU

class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ('id', 'name',)


class LPUSerializer(serializers.ModelSerializer):

    class Meta:
        model = LPU
        fields = ('id', 'name',)
