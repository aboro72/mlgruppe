from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Kunde)
admin.site.register(Schiene)
admin.site.register(Kurs)
admin.site.register(FestplattenImageNotebook)
admin.site.register(Server)
admin.site.register(Adresse)
admin.site.register(SchieneBewegung)
admin.site.register(Ansprechpartner)
admin.site.register(FestplattenImageServer)