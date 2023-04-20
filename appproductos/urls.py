from django.urls import path # Importa la función 'path' de Django para definir rutas de URL
from . import views # Importa las vistas definidas en el archivo 'views.py'

urlpatterns = [ # Se definen las URL's del sitio web y se asocian con las vistas correspondientes
    # URL para ver la lista de categorías de productos
    path('categorias/', views.verCategorias, name='categorias'), 
    # URL para ver los productos de una categoría específica
    path('productos/<str:idCategoria>', views.verProductosCategoria, name='productos'),
    # URL para ver la información de un producto específico
    path('producto/<str:idProd>', views.verProducto, name='un_producto'),
    # URL para agregar un producto al carrito de compras
    path('carro/<str:idProd>', views.agregarCarro, name='agregarCarro'),
    # URL para ver el contenido del carrito de compras
    path('carrito/', views.verCarrito, name='carrito'),
    # URL para eliminar un producto del carrito de compras
    path('eliminar/<str:id>', views.eliminarCarrito, name='eliminar'),
    # Vista para cambiar la cantidad de un producto en el carrito
    path('cambiarCantidad/', views.cambiarCantidad,name=''),
    # Ruta para procesar pagos
    path('pagar/', views.pagarCarrito, name='pagar'),        
]
