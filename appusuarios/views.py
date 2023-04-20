from django.shortcuts import render, redirect
from .models import Usuario
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import UsuarioForm
# Importamos el formulario UsuarioForm desde el archivo forms.py

def login(request):
    """
    Función que permite el inicio de sesión de un usuario en la plataforma.
    Si el usuario existe y la contraseña es correcta, inicia sesión y redirecciona
    al usuario a la página principal (home.html). En caso contrario, muestra un mensaje
    de error en la misma página de inicio de sesión.
    Argumentos:
    - request: objeto HttpRequest con los datos de la solicitud HTTP.
    Retorna:
    - Si la solicitud HTTP es GET, retorna la vista de inicio de sesión.
    - Si la solicitud HTTP es POST, retorna la vista de inicio de sesión o redirecciona a la página principal.
    """
    if request.method == 'POST':
        # Si la solicitud HTTP es un POST, se recupera el email y password enviados
        email = request.POST['email']
        password = request.POST['password']
        
        # Se autentica al usuario
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            # Si el usuario existe y la contraseña es correcta, se inicia sesión y se redirecciona a home.html
            auth.login(request, user)
            return render(request, 'home.html')
        else:
            # Si el usuario no existe o la contraseña es incorrecta, se muestra un mensaje de error en la página de inicio de sesión
            return render(request, 'usuarios/login.html', {'alarma': 'Correo o password no valido!'})
    else: 
        # Si la solicitud HTTP es un GET, se muestra la vista de inicio de sesión
        return render(request, 'usuarios/login.html')

@login_required(login_url='login')
# Se utiliza el decorador login_required para proteger la vista home.html y obligar al usuario a iniciar sesión para acceder a ella.

def logout(request):
    """
    Función que permite cerrar la sesión de un usuario en la plataforma.
    Argumentos:
    - request: objeto HttpRequest con los datos de la solicitud HTTP.
    Retorna:
    - Redirecciona al usuario a la página de inicio de sesión.
    """
    # Cerrar sesión del usuario actual
    auth.logout(request)
    # Redireccionar al usuario a la página de inicio de sesión
    return redirect('login')

# Definimos una función llamada registrar que recibe una petición del usuario
def registrar(request):
    if request.method == 'POST':
        # Si se recibió una petición POST, se crea un formulario de UsuarioForm
        form = UsuarioForm(request.POST)
        # Si el formulario es válido, se procede a registrar al usuario
        if form.is_valid():
            # Se obtienen los datos limpios del formulario
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']            
            # Se crea un username para el usuario
            username = email.split('@')[0]
            # Se verifica si ya existe un usuario con ese correo electrónico
            existe = Usuario.objects.filter(email=email).exists() 
            if not existe:
                # Si no existe, se crea el usuario y se guarda en la base de datos
                user = Usuario.objects.create_user(
                    first_name=first_name, 
                    last_name=last_name,
                    username=username, 
                    email=email, 
                    password=password
                )
                user.is_active = True
                user.save()
                # Se redirige al usuario a la página de inicio de sesión
                return render(request, 'usuarios/login.html')
        else:
            # Si el formulario no es válido, se muestra de nuevo con los errores
            return render(request, 'usuarios/registro.html', {'form': form})
    else:
        # Si no se recibió una petición POST, se muestra el formulario vacío
        form = UsuarioForm()
        return render(request, 'usuarios/registro.html', {'form': form})
