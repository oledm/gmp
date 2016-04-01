from django.contrib import admin

from .models import Organization, LPU


class LPUAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization',)


admin.site.register(Organization)
admin.site.register(LPU, LPUAdmin)
