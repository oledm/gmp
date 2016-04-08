from rest_framework import serializers

from .models import Storage

class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Storage
