# forms.py
from django import forms
from .models import WikiPage


class WikiPageForm(forms.ModelForm):
    class Meta:
        model = WikiPage
        fields = ['title', 'content', 'group']
