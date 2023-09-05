from django import forms
from pit.models import *


class KundeForm(forms.ModelForm):
    class Meta:
        model = Kunde, Ansprechpartner, Adresse
        fields = '__all__'


class SchieneForm(forms.ModelForm):
    class Meta:
        model = Schiene, FestplattenImageNotebook
        fields = '__all__'



