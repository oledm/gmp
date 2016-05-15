from rest_framework import serializers
from .models import Input

class InputSerializer(serializers.ModelSerializer):
    obj_model = serializers.JSONField()
    date = serializers.DateTimeField(required=False)


    class Meta:
        model = Input
        fields = ('obj_model', 'date')
