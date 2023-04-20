from django.urls import path
from . import views

urlpatterns = [
    # Ruta para la vista de inicio de sesión del usuario
    path('login/', views.login, name='login'),
    # Ruta para la vista de cierre de sesión del usuario
    path('logout/', views.logout, name='logout'),
    # Ruta para la vista de registro de sesión del usuario
    path('registro/', views.registrar, name='registro'),
    

]
