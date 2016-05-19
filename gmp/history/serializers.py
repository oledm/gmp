from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from .models import Input
from gmp.reports.models import Report

class InputSerializer(serializers.ModelSerializer):
    obj_model = serializers.JSONField()
    date = serializers.DateTimeField(required=False)
    report_type = serializers.SerializerMethodField()


    class Meta:
        model = Input
        fields = ('id', 'obj_model', 'date', 'report_type')

    def get_report_type(self, obj):
        return str(Report.objects.get(url=obj.obj_model.get('type')))
