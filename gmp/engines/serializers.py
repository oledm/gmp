from rest_framework import serializers

from .models import Engine

class EngineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Engine
        fields = ('name',)
