from rest_framework import serializers

from .models import FileStorage

class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileStorage
