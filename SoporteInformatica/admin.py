from django.contrib import admin
from .models import Ticket, Relacion_problema
from django.utils import timezone


class TicketAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', "get_email", "oficina", "relacion_problema", 'fecha_creacion', "estado_completado"]
    readonly_fields = ["nombre_completo", 'fecha_creacion', "mostrar_email"]
    actions = ['marcar_como_completado']


    def nombre_completo(self, obj):
        return f"{obj.usuario} {obj.usuario.last_name}".strip()
    nombre_completo.short_description = "Nombre"

    def get_email(self, obj):
            return obj.usuario.email
    get_email.short_description = 'Email'   
    
    def mostrar_email(self, obj):
        return obj.usuario.email or "-"
    mostrar_email.short_description = 'Correo del Usuario'
    
    def marcar_como_completado(self, request, queryset):
        updated = queryset.update(tarea_completada=timezone.now())
        self.message_user(request, f"{updated} ticket(s) marcados como completados.")
    marcar_como_completado.short_description = "Marcar tickets seleccionados como completados"
    
    def estado_completado(self, obj):
        return "Completado" if obj.tarea_completada else "Pendiente"
    estado_completado.short_description = "Estado"

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Relacion_problema)

