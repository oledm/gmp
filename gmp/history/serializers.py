from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from .models import Input
from gmp.reports.models import Report
from gmp.reports.serializers import ReportSerializer

class InputSerializer(serializers.ModelSerializer):
    obj_model = serializers.JSONField()
    date = serializers.DateTimeField(required=False)
    report_data = serializers.SerializerMethodField()


    class Meta:
        model = Input
        fields = ('id', 'obj_model', 'date', 'report_data')

    def get_report_data(self, obj):
        report_data = Report.objects.get(url=obj.obj_model.get('url'))
        return ReportSerializer(report_data).data
