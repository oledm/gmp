from django.contrib import admin

from .models import Engine, Connection, Factory, ExClass, WarmingClass, ThermClass
from gmp.authentication.behaviors import SuperUserAccessMixin

class EngineAdmin(SuperUserAccessMixin, admin.ModelAdmin):
    dep_name = 'Лаборатория энергосбережения и экологии'

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

class ConnectionAdmin(EngineAdmin):
    pass

class FactoryAdmin(EngineAdmin):
    pass

class ExClassAdmin(EngineAdmin):
    pass

class WarmingClassAdmin(EngineAdmin):
    pass

class ThermClassAdmin(EngineAdmin):
    pass

admin.site.register(Engine, EngineAdmin)
admin.site.register(Connection, ConnectionAdmin)
admin.site.register(Factory, FactoryAdmin)
admin.site.register(ExClass, ExClassAdmin)
admin.site.register(WarmingClass, WarmingClassAdmin)
admin.site.register(ThermClass, ThermClassAdmin)
