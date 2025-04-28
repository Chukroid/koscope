from django.urls import path # type: ignore
from . import views

app_name = 'scanner'

urlpatterns = [
    path("", views.index, name="index"),
    path("registrar-entrada/", views.registrar_entrada, name="registrar_entrada"),
    path("registrar-salida/", views.registrar_salida, name="registrar_salida"),
]