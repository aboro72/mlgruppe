from django.contrib import admin
from .models import Kunde, Schiene, Trainer, Kurs, FestplattenImage, Server, Adresse, SchieneBewegung
# Register your models here.
admin.site.register(Kunde)
admin.site.register(Schiene)
admin.site.register(Kurs)
admin.site.register(FestplattenImage)
admin.site.register(Server)
admin.site.register(Adresse)
admin.site.register(SchieneBewegung)