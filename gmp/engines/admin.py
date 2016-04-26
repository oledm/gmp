from django.contrib import admin

from .models import Engine, Connection, Factory, ExClass, WarmingClass, ThermClass
from gmp.authentication.behaviors import SuperUserAccessMixin

class EngineAdmin(SuperUserAccessMixin, admin.ModelAdmin):
    pass

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
