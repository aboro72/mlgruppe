from django.contrib import admin
from .models import Kunde, Schiene, Trainer, Kurs, FestplattenImage, Server
# Register your models here.
admin.site.register(Kunde)
admin.site.register(Schiene)
admin.site.register(Trainer)
admin.site.register(Kurs)
admin.site.register(FestplattenImage)
admin.site.register(Server)