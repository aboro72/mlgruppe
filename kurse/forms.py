from django import forms
from .models import Kurs


class KursForm(forms.ModelForm):
    class Meta:
        model = Kurs
        fields = '__all__'  # Hier kannst du die Felder auswählen, die im Formular angezeigt werden sollen
