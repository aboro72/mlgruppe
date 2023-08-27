from django.urls import path
from . import views

app_name = "textbot"

urlpatterns = [
    path("", views.home, name="home"),
    path("suggest/", views.suggest, name="suggest"),
    path("translate/", views.translate, name="translate"),
    path("past/", views.past, name="past"),
    path("delete_past/<past_id>", views.delete_past, name="delete_past"),
]

handler502 = "textbot.views.handle_502_error"
handler503 = "textbot.views.handle_502_error"

handler400 = "django.views.defaults.bad_request"
handler403 = "django.views.defaults.permission_denied"
handler404 = "django.views.defaults.page_not_found"
handler500 = "django.views.defaults.server_error"

urlpatterns += [
    path("500/", views.handle_502_error, name="502_error"),
]
"""
handler404 = 'textbot.views.handle_404_error'
handler500 = 'textbot.views.handle_500_error'
"""
