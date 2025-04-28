from django.contrib import admin # type: ignore
from .models import *

# Register your models here.
admin.site.register(Alumno)
admin.site.register(Tutor)
admin.site.register(RegistroAsistencia)