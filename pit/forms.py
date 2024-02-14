from django import forms
from .models import Abholung, Rueckholung, Versand, Schiene, Server


class AbholungForm(forms.ModelForm):
    class Meta:
        model = Abholung
        fields = '__all__'


class RueckholungForm(forms.ModelForm):
    class Meta:
        model = Rueckholung
        fields = '__all__'


class VersandForm(forms.ModelForm):

    class Meta:
        model = Versand
        fields = '__all__'


class SchieneForm(forms.ModelForm):
    class Meta:
        model = Schiene
        fields = '__all__'


class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = '__all__'