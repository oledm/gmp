from django.contrib import admin

from .models import Report
from gmp.authentication.behaviors import SuperUserAccessMixin

class ReportAdmin(SuperUserAccessMixin, admin.ModelAdmin):
    pass

admin.site.register(Report, ReportAdmin)
