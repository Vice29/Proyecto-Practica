from django import forms
from .models import Ticket
from django.contrib.auth.models import User 


class UsuarioConNombre(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        nombre = f"{obj.first_name} {obj.last_name}".strip()
        if not nombre.strip():
            nombre = obj.username
        return f"{nombre} ({obj.email})"


class FormularioSeleccionUsuario(forms.Form):
    usuario = UsuarioConNombre(
        queryset=User.objects.all().order_by("last_name", "first_name"),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Filtrar por usuario")


class FormularioSolicitud(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["oficina", "relacion_problema", "detalle" ]
        widgets = {
            "oficina": forms.TextInput(attrs={"class": "form-control", "placeholder": "Escriba su oficina."}),
            "relacion_problema": forms.Select(attrs={"class": "form-control"}),
            "detalle": forms.Textarea(attrs={"class": "form-control", "placeholder": "Añada el detalle de su problema. Por favor sea lo mas especifico posible."})
        }
    
    
