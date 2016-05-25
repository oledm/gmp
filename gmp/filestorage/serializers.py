from rest_framework import serializers

from .models import FileStorage

class FileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FileStorage
        fields = ('id', 'url', 'name', 'fileupload')
