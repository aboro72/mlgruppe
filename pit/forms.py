from django import forms
from .models import Abholung


class AbholungForm(forms.ModelForm):
    class Meta:
        model = Abholung
        fields = '__all__'
