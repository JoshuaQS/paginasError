import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser

# Formulario de creación de usuario personalizado
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'surname', 'control_number', 'password1', 'password2']

        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'pattern': '^[a-zA-Z0-9._%+-]+@utez\.edu\.mx$',
                'title': 'Por favor, ingresa un correo institucional (ejemplo: usuario@utez.edu.mx).',
                'required': True,
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'minlength': '2',
                'maxlength': '50',
                'pattern': '^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$',
                'title': 'El nombre debe tener entre 2 y 50 caracteres y solo puede contener letras.',
                'required': True,
            }),
            'surname': forms.TextInput(attrs={
                'class': 'form-control',
                'minlength': '2',
                'maxlength': '50',
                'pattern': '^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$',
                'title': 'El apellido debe tener entre 2 y 50 caracteres y solo puede contener letras.',
                'required': True,
            }),
            'control_number': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '^[0-9]{10}$',
                'title': 'La matrícula debe tener exactamente 10 dígitos.',
                'required': True,
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'minlength': '8',
                'title': 'La contraseña debe tener al menos 8 caracteres, un número y un símbolo (!, #, $, %, & o ?).',
                'required': True,
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'minlength': '8',
                'title': 'Por favor, repite la contraseña.',
                'required': True,
            }),
        }

    # Validación en el backend
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_regex = r'^[a-zA-Z0-9._%+-]+@utez\.edu\.mx$'
        if not re.match(email_regex, email):
            raise forms.ValidationError("El correo debe ser institucional (@utez.edu.mx).")
        return email

    def clean_control_number(self):
        control_number = self.cleaned_data.get('control_number')
        if not re.match(r'^[0-9]{10}$', control_number):
            raise forms.ValidationError("La matrícula debe tener exactamente 10 dígitos.")
        return control_number

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError("La contraseña debe contener al menos un número.")
        if not re.search(r'[!#$%&?]', password):
            raise forms.ValidationError("La contraseña debe contener al menos un símbolo (!, #, $, %, & o ?).")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

# Formulario de inicio de sesión personalizado
class CustomUserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'pattern': '^[a-zA-Z0-9._%+-]+@utez\.edu\.mx$',
            'title': 'Por favor, ingresa un correo institucional (ejemplo: usuario@utez.edu.mx).',
            'required': True,
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'minlength': '8',
            'title': 'La contraseña debe tener al menos 8 caracteres.',
            'required': True,
        })
    )
