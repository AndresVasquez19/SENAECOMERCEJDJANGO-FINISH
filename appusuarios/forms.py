# Importar la clase Form del módulo forms de Django y la clase Usuario del modelo.
from django import forms
from .models import Usuario

# Definir la clase UsuarioForm como una subclase de ModelForm.
class UsuarioForm(forms.ModelForm):
    """
    Formulario para crear un objeto Usuario a partir de los campos de un modelo Usuario.
    """
    class Meta:
        model = Usuario
        # Campos del modelo que se incluirán en el formulario.
        fields = ['first_name', 'last_name', 'email', 'password']
        # Etiquetas para cada campo del formulario.
        labels = {
            'first_name': 'Nombre: ',
            'last_name': 'Apellido: ',
            'email': 'Correo E: ',
            'password': 'Contraseña: ',
        }


