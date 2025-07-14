from django import forms
from .models import Ticket

class FormularioSolicitud(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["oficina", "relacion_problema", "detalle" ]
        widgets = {
            "oficina": forms.TextInput(attrs={"class": "form-control", "placeholder": "Escriba su oficina."}),
            "relacion_problema": forms.Select(attrs={"class": "form-control"}),
            "detalle": forms.Textarea(attrs={"class": "form-control", "placeholder": "Añada el detalle de su problema. Por favor sea lo mas especifico posible."})
        }