import threading
import locale
import requests
import urllib.parse
from django.utils.timezone import localtime #type: ignore
from django.utils import timezone # type: ignore
from decouple import config
from django.shortcuts import render,HttpResponse # type: ignore
from django.http import JsonResponse # type: ignore
from registros.models import Alumno,RegistroAsistencia,Tutor
from django.forms.models import model_to_dict # type: ignore
from django.core.mail import send_mail #type: ignore
from twilio.rest import Client

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8') # para cambiar el local a español (como los meses y dias)
account_sid = config('TWILIO_SID')
auth_token = config('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

# FUNCIONES CUTOMIZADOS
def serializar_Alumno(alumno:Alumno): # este es una funcion que transformara un modelo de Alumno a un diccionario
    alumnoDict = model_to_dict(alumno)

    # si hay imagenes, nada mas guardar los urls de las imagenes
    if alumno.imagen_alumno:
        alumnoDict["imagen_alumno"] = alumno.imagen_alumno.url
    else:
        alumnoDict["imagen_alumno"] = None
    if alumno.qr_code:
        alumnoDict["qr_code"] = alumno.qr_code.url
    else:
        alumnoDict["qr_code"] = None

    return alumnoDict

def enviar_correo(titulo,mensaje,from_correro,to_correo): # funcion para enviar correos sin que demore el codigo
    threading.Thread(target=send_mail, args=(titulo, mensaje, from_correro, to_correo)).start()


def combinar_alumno(alumno:Alumno):
    return alumno.apellido_paterno+((" "+alumno.apellido_materno) if alumno.apellido_materno else "")+" "+alumno.nombre


# Create your views here.
def index(request):
    return render(request, "scanner_index.html")


# APIS
def buscar_alumno(request): # para buscar alumno en la base de datos usando el id 
    matricula = request.GET.get("matricula")
    try:
        alumno = Alumno.objects.get(matricula=matricula)

        return alumno
    except Alumno.DoesNotExist:
        return
    
def registrar_entrada(request):    
    # buscar el alumno primero
    alumno = buscar_alumno(request)
    forzado = request.GET.get("forced","false").lower() == "true"

    # si existe, registrar su asistencia y regresar su identificador (ID)
    if alumno:

        # buscar su ultimo registro y checar si su ultimo registro, ya habia registrado su salida
        ultimo_registro = alumno.ultimo_registro()
        if not forzado:
            if ultimo_registro and ultimo_registro.salida_hora_fecha == None:
                return JsonResponse({"error": "Ese alumno no registro su salida posteriormente"}, status=400)
            

        # registrar la asistencia
        asistenciaRegistro = RegistroAsistencia.objects.create(
            alumno=alumno,
            entrada_registrada=True,
            salida_registrada=False
        )
        tutor = Tutor.objects.get(matriculo_alumno=alumno.matricula)
        if tutor:
            tiempoTexto = localtime(timezone.now())
            mensaje = "Hola "+tutor.nombre_tutor+", El alumno "+combinar_alumno(alumno)+" de Grado "+str(alumno.grado)+" y Grupo "+alumno.grupo+", acaba de registrar una entrada el "+tiempoTexto.strftime("%A, %d de %B a las %I:%M %p")+"."
            enviar_correo(
                "Nueva Entrada Registrada!",
                mensaje,
                config('CORREO_USUARIO'),
                [tutor.correo_electronico_tutor], 
            )

        # regresar el dato del alumno
        alumnoSerializado = serializar_Alumno(alumno)
        alumnoSerializado["EntradaRegistrada"] = True
        alumnoSerializado["TiempoRegistrado"] = localtime(asistenciaRegistro.entrada_hora_fecha).strftime("%I:%M %p")
        return JsonResponse({"alumno": alumnoSerializado,"message": "Entrada Registrada correctamente!"})
    else:
        return JsonResponse({"error": "Alumno no encontrado"}, status=400)

def registrar_salida(request):
    # buscar el alumno primero
    alumno = buscar_alumno(request)
    forzado = request.GET.get("forced","false").lower() == "true"

    # si existe
    if alumno:
        
        # buscar su ultimo registro
        ultimo_registro = alumno.ultimo_registro()
        if not ultimo_registro:
            if not forzado:
                return JsonResponse({"error": "Este Alumno no registro su entrada"}, status=400)
            else:
                ultimo_registro =  RegistroAsistencia.objects.create(
                    alumno=alumno,
                    entrada_registrada=True,
                    salida_registrada=False
                )

       # checar si ya habia registrado su salida
        if not forzado and ultimo_registro.salida_hora_fecha:
            return JsonResponse({"error": "Este alumno ya habia registrado su salida"}, status=400)
        
        # modificar su salida
        ultimo_registro.salida_hora_fecha = timezone.now()
        ultimo_registro.salida_registrada = True
        ultimo_registro.save()

        tutor = Tutor.objects.get(matriculo_alumno=alumno.matricula)
        if tutor:
            tiempoTexto = localtime(timezone.now())
            mensaje = "Hola "+tutor.nombre_tutor+", El alumno "+combinar_alumno(alumno)+" de Grado "+str(alumno.grado)+" y Grupo "+alumno.grupo+", acaba de registrar su salida el "+tiempoTexto.strftime("%A, %d de %B a las %I:%M %p")+"."
            enviar_correo(
                "Salida Registrada!",
                mensaje,
                config('CORREO_USUARIO'),
                [tutor.correo_electronico_tutor], 
            )

        # regresar el dato del alumno
        alumnoSerializado = serializar_Alumno(alumno)
        alumnoSerializado["TiempoRegistrado"] = localtime(ultimo_registro.salida_hora_fecha).strftime("%I:%M %p")
        return JsonResponse({"alumno": alumnoSerializado,"message": "Salida Registrada correctamente!"})
    else:
        return JsonResponse({"error": "Alumno no encontrado"}, status=400)