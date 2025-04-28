from django.urls import path
from . import views

app_name = "estadisticas"

urlpatterns = [
    path("",views.index,name="index"),
    path("registro_totales/",views.registros_totales,name="registro_totales"),
    path("registro_generos/",views.registros_por_genero,name="registro_generos")
]