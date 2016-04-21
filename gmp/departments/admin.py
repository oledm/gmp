from django.contrib import admin

from .models import Measurer, Department


class MeasurerAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'department',)


# Register your models here.
admin.site.register(Measurer, MeasurerAdmin)
admin.site.register(Department)
