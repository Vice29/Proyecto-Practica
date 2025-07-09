from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Relacion_problema(models.Model):
    tipo = models.CharField(max_length=100)

    def __str__(self):
        return self.tipo


class Ticket(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    correo = models.EmailField(null=True, blank=True)
    nombre = models.CharField(max_length=100)
    oficina = models.CharField(max_length=100)
    detalle = models.TextField()
    relacion_problema = models.ForeignKey(Relacion_problema, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    tarea_completada = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombre} - {self.usuario}"

