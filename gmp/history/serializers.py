from django.contrib.humanize.templatetags.humanize import naturaltime

from rest_framework import serializers

from .models import Input
from gmp.reports.models import Report

class InputSerializer(serializers.ModelSerializer):
    obj_model = serializers.JSONField()
    date = serializers.DateTimeField(required=False)
    report_type = serializers.SerializerMethodField()


    class Meta:
        model = Input
        fields = ('obj_model', 'date', 'report_type')

    def get_report_type(self, obj):
        try:
            rep = str(Report.objects.get(url=obj.obj_model.get('type')))
        except AttributeError:
            rep = ''
        return rep

