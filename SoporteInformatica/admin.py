from django.contrib import admin
from .models import Ticket, Relacion_problema

class TicketAdmin(admin.ModelAdmin):
    list_display = ['usuario' ,"correo",'nombre', "oficina", "relacion_problema", 'fecha_creacion']
    readonly_fields = ['fecha_creacion'] 

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Relacion_problema)
