from django import forms
from pit.models import *
from kunden.models import *
from kurse.models import *


class KundeForm(forms.ModelForm):
    class Meta:
        model = Kunde, Ansprechpartner, Adresse
        fields = '__all__'


class SchieneForm(forms.ModelForm):
    class Meta:
        model = Schiene, FestplattenImageNotebook
        fields = '__all__'


class KurseForm(forms.ModelForm):
    class Meta:
        model = Kurs
        fields = '__all__'
