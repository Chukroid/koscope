from django.shortcuts import render, redirect, HttpResponse, get_object_or_404 # type: ignore
from .models import Alumno,Tutor
from django.contrib.auth.forms import UserCreationForm # type: ignore
from .registroForm import AlumnoRegistrationForm,TutorRegistroForm,RegistrationForm



# Create your views here.
def agregar(request):
    if request.method == 'POST':
        registroform = RegistrationForm()
        registroform.alumnoform = AlumnoRegistrationForm(request.POST, request.FILES)
        registroform.tutorform = TutorRegistroForm(request.POST)
        if registroform.is_valid():
            alumno,tutor = registroform.save(request.user)
            tutor.matriculo_alumno = alumno.matricula
            registroform.save(request.user)

            request.session["sub_info"] = {
                "mensaje": "El alumno "+alumno.apellido_paterno+(" "+alumno.apellido_materno if alumno.apellido_materno else "")+" "+alumno.nombre+" ha sido registrado correctamente",
                "status": "ok"
            }

            return redirect('registros:Alumno', alumno_id=alumno.id_alumno)
    else:
        registroform = RegistrationForm()
        registroform.alumnoform = AlumnoRegistrationForm()
        registroform.tutorform = TutorRegistroForm()
    return render(request, "agregar.html",{'form': registroform})

def mostrar(request,alumno_id):
    alumno = get_object_or_404(Alumno, pk=alumno_id)
    tutor = Tutor.objects.filter(matriculo_alumno=alumno.matricula).first()
    sub_info = request.session.pop('sub_info', None)  # gets and removes it

    return render(request, 'mostrar.html', {
        'alumno': alumno,
        'tutor': tutor,
        'sub_info': sub_info
    })

def panel(request):
    return render(request,'dashboard.html')