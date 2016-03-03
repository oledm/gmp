from django.contrib import admin

from .models import Engine, Connection, Factory, ExClass, WarmingClass

admin.site.register(Engine)
admin.site.register(Connection)
admin.site.register(Factory)
admin.site.register(ExClass)
admin.site.register(WarmingClass)