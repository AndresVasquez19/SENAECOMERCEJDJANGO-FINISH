 
 # Importa el módulo admin y los modelos
from django.contrib import admin
from .models import *
# Register your models here.


# Registra los modelos en el panel de administración
# Define las columnas que se mostrarán en la lista de categorías
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripCategoria']

# Registra el modelo Categoria junto con la configuración de administración
admin.site.register(Categoria, CategoriaAdmin)

# Define las columnas que se mostrarán en la lista de productos
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'existencia']

# Registra el modelo Producto junto con la configuración de administración
admin.site.register(Producto, ProductoAdmin)

# Define las columnas que se mostrarán en la lista de carros
class CarroAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'producto', 'cantidad', 'estado']

# Registra el modelo Carro junto con la configuración de administración
admin.site.register(Carro, CarroAdmin)
