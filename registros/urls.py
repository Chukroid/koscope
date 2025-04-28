from django.urls import path # type: ignore
from . import views

app_name = 'registros'

urlpatterns = [
    path("", views.agregar, name="index"),
    path("alumno/<int:alumno_id>/", views.mostrar, name="Alumno"),
]