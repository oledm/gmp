from django.contrib import admin

from .models import Instrument, Department

# Register your models here.
admin.site.register(Instrument)
admin.site.register(Department)
