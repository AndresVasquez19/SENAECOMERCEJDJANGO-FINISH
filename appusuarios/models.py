from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Define un gestor de usuario personalizado para el modelo de usuario personalizado.
class MyAccountManager(BaseUserManager):
    # Método para crear un usuario.
    def create_user(self, first_name, last_name, email, username, password=None):
        # Si el correo electrónico o el nombre de usuario no se proporcionan, levanta una excepción.
        if not email:
            raise ValueError('El usuario debe tener un correo')
        if not username:
            raise ValueError('El usuario debe tener un username')
        
        # Crea un nuevo usuario con los atributos proporcionados.
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        # Configura la contraseña para el usuario y lo guarda en la base de datos.
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Método para crear un superusuario.
    def create_superuser(self, first_name, last_name, email, username, password):
        # Crea un nuevo usuario con los atributos proporcionados.
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        # Configura los atributos de superusuario para el usuario y lo guarda en la base de datos.
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

# Define el modelo de usuario personalizado.
class Usuario(AbstractBaseUser):
    # Definir las opciones de rol que un usuario puede tener.
    ROLES = (
        ('admin', 'admin'),
        ('cliente', 'cliente'),
    )
    # Define los atributos del usuario.
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    rol = models.CharField(max_length=30, choices=ROLES, default='cliente')

    # Define los atributos de Django.
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    # Métodos para comprobar los permisos del usuario.
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    # Método para obtener una representación en cadena del usuario.
    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    # Define los metadatos del modelo.
    class Meta:
        verbose_name_plural = "Usuarios" 
