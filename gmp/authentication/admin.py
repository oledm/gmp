from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.models import User, Group

from .models import Employee
from .behaviors import SuperUserAccessMixin

class EmployeeAdmin(SuperUserAccessMixin, admin.ModelAdmin):
    list_display = ('get_full_name', 'department', 'email',)

admin.site.register(Employee, EmployeeAdmin)
admin.site.unregister(Site)
admin.site.unregister(Group)

admin.site.site_title = 'Администрирование АКФОД'
admin.site.site_header = 'Администрирование АКФОД'
