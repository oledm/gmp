from django.contrib import admin
from .models import Container, Factory, Carrier, Material, Welding, Control
from gmp.authentication.behaviors import SuperUserAccessMixin

class ContainerAdmin(SuperUserAccessMixin, admin.ModelAdmin):
    dep_name = 'Отдел оборудования работающего под давлением'

    def get_queryset(self, request):
        if request.user.department.name == self.dep_name:
            return self.model.objects.all()
        else:
            return super().get_queryset(request)

    def get_model_perms(self, request):
        if request.user.department.name == self.dep_name:
            return {'change': True, 'add': True, 'delete': True}
        else:
            return super().get_model_perms(request)

class FactoryAdmin(ContainerAdmin, admin.ModelAdmin):
    pass

class CarrierAdmin(ContainerAdmin, admin.ModelAdmin):
    pass

class MaterialAdmin(ContainerAdmin, admin.ModelAdmin):
    pass

class WeldingAdmin(ContainerAdmin, admin.ModelAdmin):
    pass

class ControlAdmin(ContainerAdmin, admin.ModelAdmin):
    pass

admin.site.register(Container, ContainerAdmin)
admin.site.register(Factory, FactoryAdmin)
admin.site.register(Carrier, CarrierAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Welding, WeldingAdmin)
admin.site.register(Control, ControlAdmin)
