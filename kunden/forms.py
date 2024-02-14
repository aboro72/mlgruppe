from django import forms
from .models import Kunde
from start.forms import AdresseForm

class KundeForm(forms.ModelForm):
    class Meta:
        model = Kunde
        fields = '__all__'

    # Überschreibt die __init__ Methode, um das AdresseForm hinzuzufügen
    def __init__(self, *args, **kwargs):
        super(KundeForm, self).__init__(*args, **kwargs)
        self.adresse_form = AdresseForm()

    # Überschreibt die save Methode, um das Speichern von Kunde und Adresse zu verarbeiten
    def save(self, commit=True):
        kunde_instance = super(KundeForm, self).save(commit=False)
        adresse_instance = self.adresse_form.save(commit=False)
        if commit:
            kunde_instance.save()
            adresse_instance.kunde = kunde_instance  # Annahme: ForeignKey oder OneToOneField von Adresse zu Kunde
            adresse_instance.save()
        return kunde_instance
