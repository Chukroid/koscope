from django import forms # type: ignore
from .models import Alumno,Tutor

class AlumnoRegistrationForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = '__all__'
        exclude = ['qr_code'] 

class TutorRegistroForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = '__all__'
        exclude = ['matriculo_alumno'] 

class RegistrationForm(forms.Form):
    alumnoform = AlumnoRegistrationForm()
    tutorform = TutorRegistroForm()

    def is_valid(self):
        return self.alumnoform.is_valid() and self.tutorform.is_valid()

    def save(self, user):
        alumno = self.alumnoform.save()

        tutor = self.tutorform.save()
        return alumno,tutor

