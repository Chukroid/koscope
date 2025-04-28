from django.shortcuts import render
from django.http import JsonResponse
from registros.models import RegistroAsistencia
from django.utils import timezone
from django.db.models.functions import TruncDay,TruncWeek, TruncMonth
from django.db.models import Count
from datetime import timedelta
from django.utils.timezone import localtime

# Charts
# hoy (per dia)
# ultima semana (per semana)
# ultimo mes (per mes)

# numero de entradas 
# numero de entradas donde salida fue registrada

# numero de entradas hombre
# numero de entradas donde salida fue registrada hombre
# numero de entradas mujeres
# numero de entradas donde salida fue registrada mujeres


def serializar_listas(datos): # una funcion que convertirar las listas que obtenemos a json
    lista_formateada = {
            day_data['periodo'].strftime('%-d de %B'): day_data['count']
            for day_data in datos
        }
    return lista_formateada

def obtener_estadisticas_por_periodo(periodo, entrada_filtros,salida_filtros): # funcion para obtener listas de datos por periodos
    if entrada_filtros is None:
        entrada_filtros = {}
    if salida_filtros is None:
        salida_filtros = {}
    hoy = localtime(timezone.now())

    if periodo == "d":
        trunc_func = TruncDay
        fecha_inicio = hoy - timedelta(days=5)
        tiempo_contador = hoy.date()
    elif periodo == "w":
        t = hoy - timedelta(days=hoy.weekday())
        trunc_func = TruncWeek
        fecha_inicio = hoy - timedelta(weeks=5)
        tiempo_contador = t.date()
    elif periodo == "m":
        trunc_func = TruncMonth
        fecha_inicio = hoy - timedelta(days=30 * 5)
        tiempo_contador = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # estoy usando __gte para que pueda filtrar bien osea, si la fecha es menor que hace 5 semanda,etc
    total_entradas = RegistroAsistencia.objects.filter(entrada_hora_fecha__gte=tiempo_contador,**entrada_filtros)
    total_salidas = RegistroAsistencia.objects.filter(entrada_hora_fecha__gte=tiempo_contador,**salida_filtros)

    entradas = (
            RegistroAsistencia.objects
            .filter(entrada_hora_fecha__gte=fecha_inicio, **entrada_filtros)
            .annotate(periodo=trunc_func('entrada_hora_fecha'))
            .values('periodo')
            .annotate(count=Count('id_registro'))
            .order_by('periodo')
        )

    salidas = (
        RegistroAsistencia.objects
        .filter(entrada_hora_fecha__gte=fecha_inicio, **salida_filtros)
        .annotate(periodo=trunc_func('entrada_hora_fecha'))
        .values('periodo')
        .annotate(count=Count('id_registro'))
        .order_by('periodo')
    )

    return total_entradas.count(),total_salidas.count(),entradas, salidas

# Create your views here.
def index(request):
    return render(request, 'estadistica_index.html')

def registros_totales(request):
    filtro = request.GET.get("filtro","d")

    total_entradas,total_salidas,entradas_lista,salidas_lista = obtener_estadisticas_por_periodo(filtro,{
        "entrada_registrada":True,
    },{
        "entrada_registrada":True,
        "salida_registrada":True
    })

    datos = {
        "total_entradas_1": total_entradas,
        "total_salidas_1": total_salidas,
        "entrada_lista_1": serializar_listas(entradas_lista),
        "salidas_lista_1": serializar_listas(salidas_lista)
    }

    return JsonResponse(datos,status=200)

def registros_por_genero(request):
    filtro = request.GET.get("filtro","d")

    # hombres
    total_entradas_1,total_salidas_1,entradas_lista_1,salidas_lista_1 = obtener_estadisticas_por_periodo(filtro,{
        "entrada_registrada":True,
        "alumno__genero":"H"
    },{
        "entrada_registrada":True,
        "salida_registrada":True,
        "alumno__genero":"H"
    })
    # mujeres
    total_entradas_2,total_salidas_2,entradas_lista_2,salidas_lista_2 = obtener_estadisticas_por_periodo(filtro,{
        "entrada_registrada":True,
        "alumno__genero":"M"
    },{
        "entrada_registrada":True,
        "salida_registrada":True,
        "alumno__genero":"M"
    })

    datos = {
        "total_entradas_1": total_entradas_1,
        "total_entradas_2": total_entradas_2,
        "total_salidas_1": total_salidas_1,
        "total_salidas_2": total_salidas_2,
        "entrada_lista_1": serializar_listas(entradas_lista_1),
        "entrada_lista_2": serializar_listas(entradas_lista_2),
        "salidas_lista_1": serializar_listas(salidas_lista_1),
        "salidas_lista_2": serializar_listas(salidas_lista_2)
    }

    return JsonResponse(datos,status=200)