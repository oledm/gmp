from django.contrib import admin

# Register your models here.
from .models import Certificate, ControlType, EBcertificate

admin.site.register(Certificate)
admin.site.register(ControlType)
admin.site.register(EBcertificate)
