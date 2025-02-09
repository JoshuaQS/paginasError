from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomUserLoginForm
from django.contrib.auth.decorators import login_required
import json
from .message import Message  # Importamos la clase correctamente

def register_view(request):
    message_data = None  # Inicializamos el mensaje para el modal

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Iniciar sesión después del registro
            return redirect('home')  # Redirigir a la página principal
        else:
            # Si hay errores en el formulario, los enviamos al modal
            errors = form.errors.as_json()
            message_data = Message("error", "Errores en el registro", 400, None)
            message_data = json.dumps({"tipo": "error", "mensaje": "Errores en el registro", "codigo": 400, "errores": errors})
    
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form, "message": message_data})

def login_view(request):
    message_data = None  # Inicializamos el mensaje para el modal

    if request.method == 'POST':
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            # Si el login falla, mostramos un mensaje de error
            message_data = Message("error", "Usuario o contraseña incorrectos.", 401)
            message_data = json.dumps(message_data.to_dict())

    else:
        form = CustomUserLoginForm()
    
    return render(request, 'login.html', {'form': form, "message": message_data})

def logout_view(request):
    logout(request)
    msg = Message("info", "Se ha cerrado sesión exitosamente", 200, 
                  "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR8MIbugIhZBykSmQcR0QPcfnPUBOZQ6bm35w&s")
    
    return render(request, "login.html", {"message": json.dumps(msg.to_dict())})

@login_required
def home_view(request):
    return render(request, 'home.html')
