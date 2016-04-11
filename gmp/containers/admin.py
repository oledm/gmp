from django.contrib import admin
from .models import Container, Factory, Carrier, Material, Welding, Control

admin.site.register(Container)
admin.site.register(Factory)
admin.site.register(Carrier)
admin.site.register(Material)
admin.site.register(Welding)
admin.site.register(Control)
