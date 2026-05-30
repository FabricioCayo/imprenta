from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

from .models import OrdenTrabajo


# =====================================
# FORMULARIO DE ÓRDENES DE TRABAJO
# =====================================
class OrdenTrabajoForm(forms.ModelForm):

    class Meta:

        model = OrdenTrabajo

        fields = [
            'empresa',
            'cliente',
            'telefono',
            'descripcion',
            'estado',
            'prioridad',
            'precio',
            'adelanto',
            'tiempo_estimado',
            'trabajador',
            'observaciones',
        ]

        widgets = {

            'descripcion': forms.Textarea(
                attrs={'rows': 4}
            ),

            'observaciones': forms.Textarea(
                attrs={'rows': 3}
            ),

        }


# =====================================
# FORMULARIO DE CREACIÓN DE USUARIOS
# =====================================
class UsuarioForm(UserCreationForm):

    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all()
    )

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'grupo',
        ]