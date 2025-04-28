from django.db import models # type: ignore
import os
import qrcode  # type: ignore
from django.db import models  # type: ignore
from django.core.files import File  # type: ignore
from io import BytesIO

# Create your models here.

class Alumno(models.Model):
    HOMBRE = 'H'
    MUJER = 'M'
    Generos = [
        ('', 'Seleccionar un genero:'),
        (HOMBRE, 'Hombre'),
        (MUJER, 'Mujer')
    ]

    id_alumno = models.BigAutoField(primary_key=True)
    matricula = models.CharField(max_length=200,null=True)
    nombre = models.CharField(max_length=200,null=True)
    apellido_paterno = models.CharField(max_length=200,null=True)
    apellido_materno = models.CharField(max_length=200,null=True,blank=True)
    genero = models.CharField(max_length=1,choices=Generos,null=True)
    grado = models.IntegerField(null=True)
    grupo = models.CharField(max_length=10,null=True)
    telefono = models.IntegerField(null=True)
    imagen_alumno = models.ImageField(upload_to='imagenes_alumnos/',null=True)
    correo_electronico = models.CharField(max_length=200,null=True)

    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    def save(self, *args, **kwargs):
        # Automatically generate a QR code when saving the Alumno
        if not self.qr_code:
            qr_data = self.matricula  # Use matricula or any field you prefer
            qr_image = qrcode.make(qr_data)

            # Save the QR code to a file-like object (BytesIO)
            qr_image_file = BytesIO()
            qr_image.save(qr_image_file)
            qr_image_file.seek(0)
            
            # Create a Django File object
            self.qr_code.save(f"qr_code_{self.matricula}.png", File(qr_image_file), save=False)
        
        super().save(*args, **kwargs)
    
    def ultimo_registro(self):
        return self.registros.order_by('-entrada_hora_fecha').first()

class Tutor(models.Model):
    id_tutor = models.BigAutoField(primary_key=True)
    matriculo_alumno = models.CharField(max_length=200,null=True)
    nombre_tutor = models.CharField(max_length=200,null=True)
    apellido_paterno_tutor = models.CharField(max_length=200,null=True)
    apellido_materno_tutor = models.CharField(max_length=200,null=True)
    telefono_tutor = models.IntegerField(null=True)
    correo_electronico_tutor = models.CharField(max_length=200,null=True)

class RegistroAsistencia(models.Model):
    id_registro = models.BigAutoField(primary_key=True)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='registros')
    entrada_hora_fecha = models.DateTimeField(auto_now_add=True)
    salida_hora_fecha = models.DateTimeField(null=True,blank=True)
    entrada_registrada = models.BooleanField(default=True)
    salida_registrada = models.BooleanField(default=False)