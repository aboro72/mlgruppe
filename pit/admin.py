from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Schiene)
admin.site.register(FestplattenImageNotebook)
admin.site.register(Server)
admin.site.register(FestplattenImageServer)
admin.site.register(Abholung)