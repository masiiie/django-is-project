from django import forms
from .models import *
import django.forms.widgets as wd

class LugarForm(forms.ModelForm):
    """Form definition for Lugar"""
    solicitud = forms.ModelChoiceField(queryset = Solicitud.objects.all())
    class Meta:
        """Meta definition for Lugarform"""
        model = Lugar
        exclude = ("chequeado","precio_de_subasta","evaluacion")

class CuartoForm(forms.ModelForm):
    """Form definition for Cuarto"""

    class Meta:
        """Meta definition for Cuartoform."""
        model = Cuarto
        exclude = ()

class TagForm(forms.ModelForm):
    """Form definition for Tag"""

    class Meta:
        """Meta definition for Tagform."""
        model = Tag
        exclude = ()

class SolicitudForm(forms.ModelForm):
    """Form definition for Solicitud"""

    class Meta:
        """Meta definition for SolicitudForm."""
        model = Solicitud
        exclude = ("tiempo","chequeado","perito",)

class ClientUserForm(forms.ModelForm):
    """Form definition for User"""

    class Meta:
        """Meta definition for ClientUserform."""
        model = User
        fields = ('first_name','last_name','email',)

class StaffUserForm(forms.ModelForm):
    """Form definition for User"""

    class Meta:
        """Meta definition for StaffUserForm."""
        model = User
        fields = ('username','password','first_name','last_name','email','groups')

