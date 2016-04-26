from django.contrib import admin

from .models import Measurer, Department
from gmp.authentication.behaviors import SuperUserAccessMixin


class MeasurerAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'department',)


class DepartmentAdmin(SuperUserAccessMixin, admin.ModelAdmin):
    pass

# Register your models here.
admin.site.register(Measurer, MeasurerAdmin)
admin.site.register(Department, DepartmentAdmin)
