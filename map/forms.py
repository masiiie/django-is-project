from django import forms
from inmobiliaria.models import provinceChoice
# from inmobiliaria.models import *

class FindPlaces_alquiler(forms.Form):
    renta_linear = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class":"event_search"}))
    renta_de_cuartos =forms.BooleanField(widget=forms.CheckboxInput(attrs={"class":"event_search"}))
    min_precioAlquiler= forms.IntegerField(widget=forms.NumberInput(),initial=20) 
    max_precioAlquiler= forms.IntegerField(widget=forms.NumberInput,initial=1000) 
    

class FindPlaces_venta(forms.Form):
    venta= forms.BooleanField(widget=forms.CheckboxInput(attrs={"class":"event_search"}))
    subastable=forms.BooleanField(widget=forms.CheckboxInput(attrs={"class":"event_search"}))
    min_precioVenta= forms.IntegerField(widget=forms.NumberInput,initial=3000)
    max_precioVenta= forms.IntegerField(widget=forms.NumberInput,initial=900000)

class GenericSearch(forms.Form):
    provincia=forms.CharField(widget=forms.Select(choices=provinceChoice))
    buscar_Area= forms.BooleanField(widget=forms.CheckboxInput())