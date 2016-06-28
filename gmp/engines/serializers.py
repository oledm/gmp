from rest_framework import serializers

from .models import Engine, ThermClass, Connection

class EngineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Engine
        fields = ('name',)


class TClassSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = ThermClass
        fields = ('id', 'name',)

    def get_name(self, obj):
        return obj.get_name_display()


class ConnectionTypesSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Connection
        fields = ('id', 'name',)

    def get_name(self, obj):
        return obj.get_connection_type_display()

