import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# Función para mostrar las categorías de productos
def verCategorias(request):
    #Consultar categorias
    listaCateg = Categoria.objects.all()

    # Ensamblar context
    context = {
        'categorias': listaCateg,
        'titulo': 'Categorias de Productos del Supermercado',
    }

    # Renderizar la plantilla 'categorias.html' con el contexto creado
    return render(request, 'productos/categorias.html', context) 
from django.shortcuts import render
     
def verProductosCategoria(request, idCategoria):
    """
    Esta función muestra todos los productos que pertenecen a una categoría específica.
    Argumentos:
        request: objeto HttpRequest que representa la solicitud del usuario.
        idCategoria: entero que representa el identificador de la categoría.

    Retorna:
        Un objeto HttpResponse con la lista de productos y el título de la página.
    """
    # Convertir idCategoria a entero
    idCat = int(idCategoria)
    # Obtener la categoría correspondiente
    nombreCat = Categoria.objects.get(id=idCat) 
    # Filtrar productos por categoría
    listaProductos = Producto.objects.filter(categoria= idCat)
  
    # Ensamblar contexto
    context = {
        'productos': listaProductos,
        'titulo': 'Productos de la categoría ' + str(nombreCat),
    }
    # Renderizar la plantilla y devolver una respuesta HTTP
    return render(request, 'productos/productos.html', context)

def verProducto(request, idProd, msj = None):
    """
    Vista que muestra los detalles de un producto.
    Recibe una solicitud HTTP (request) y el identificador de un producto (idProd) para mostrar sus detalles.
    También puede recibir un mensaje opcional (msj) para mostrar en la plantilla.
    Retorna una respuesta HTTP con la plantilla 'productos/producto.html' y un contexto con los detalles del producto.
    """
    # Convertir el identificador del producto a un número entero
    idProd = int(idProd)
    # Consultar la base de datos para obtener los detalles del producto correspondiente al identificador
    regProducto = Producto.objects.get(id= idProd)
    # Ensamblar el contexto con los detalles del producto y el título de la página
    context = {
        'producto': regProducto,
        'titulo': 'Detalles de ' + str(regProducto.nombre),
    }
    # Si se proporciona un mensaje, agregarlo al contexto
    if msj:
        context['mensaje']=  msj
    # Renderizar la plantilla 'productos/producto.html' con el contexto y retornar una respuesta HTTP
    return render(request, 'productos/producto.html', context)

def agregarCarro(request, idProd):
    # Convertir el parámetro idProd a entero
    idProd = int(idProd)
    # Obtener el usuario registrado
    regUsuario = request.user
    msj = None
    # Verificar si el producto existe en la base de datos
    existe = Producto.objects.filter(id=idProd).exists()
    if existe:
        # Obtener el registro del producto en la tabla Producto
        regProducto = Producto.objects.get(id=idProd)
        # Si el producto no existe en el carrito:
        existe = Carro.objects.filter(producto=regProducto, estado='activo', usuario=regUsuario).exists()
        if existe:
            # Obtener el registro del carrito correspondiente al producto y usuario
            regCarro = Carro.objects.get(producto=regProducto, estado='activo', usuario=regUsuario)
            # Incrementar la cantidad del producto en el carrito
            regCarro.cantidad += 1
        else:
            # Crear un nuevo registro en la tabla Carro para el producto
            regCarro = Carro(producto=regProducto, usuario=regUsuario, valUnit=regProducto.precioUnitario)
        # Guardar el registro en la tabla Carro
        regCarro.save()
    else:
        # Si el producto no existe, mostrar un mensaje de error
        msj = 'Producto no disponible'
    # Redireccionar a la vista verProducto
    return verProducto(request, idProd, msj)

def verCarrito(request):
    # Se llama a la función consultarCarro para obtener los productos en el carrito del usuario actual
    context = consultarCarro(request)
    # Se renderiza el template 'productos/carrito.html' con los datos obtenidos en el contexto
    return render(request, 'productos/carrito.html', context) 

def eliminarCarrito(request, id):
    # Se busca el registro del carrito con el id dado
    regCarrito = Carro.objects.get(id=id)
    # Se cambia el estado del registro a 'anulado'
    regCarrito.estado = 'anulado'
    # Se guarda el registro en la base de datos
    regCarrito.save()
    # Se redirige a la vista del carrito para actualizar la información
    return verCarrito(request)

def cambiarCantidad(request):
    # Verifica si la petición es una solicitud Ajax
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        # Verifica que el método de la petición sea POST
        if request.method == 'POST':
            # Toma la data enviada por el cliente en formato JSON
            data = json.load(request)
            id = data.get('id')
            cantidad = int(data.get('cantidad'))
            # Verifica que la cantidad sea mayor que cero
            if cantidad > 0:
                # Lee el registro y lo modifica con la nueva cantidad
                regProducto = Carro.objects.get(id=id)
                regProducto.cantidad = cantidad 
                regProducto.save()
            # Consulta el carrito actualizado
            context = consultarCarro(request)
            # Devuelve la respuesta en formato JSON
            return JsonResponse(context)
        # Devuelve un error si la petición no es POST
        return JsonResponse({'alarma': 'no se pudo modificar...'}, status=400)
    else:
        # Si no es una solicitud Ajax, redirige a la vista del carrito
        return verCarrito(request)

def consultarCarro(request):
    # Obtiene el usuario actual
    regUsuario = request.user
    # Filtra los productos de ese usuario en estado 'activo'
    listaCarrito = Carro.objects.filter(usuario=regUsuario, estado='activo').values('id', 'cantidad', 'valUnit', 'producto__imgPeque', 'producto__nombre', 'producto__unidad', 'producto__id')
    # Crea una lista de diccionarios con los productos del carrito
    listado = []
    subtotal = 0
    for prod in listaCarrito:
        reg = {
            'id': prod['id'],
            'cantidad': prod['cantidad'],
            'valUnit': prod['valUnit'],
            'imgPeque': prod['producto__imgPeque'],
            'nombre': prod['producto__nombre'],
            'unidad': prod['producto__unidad'],
            'total': prod['valUnit'] * prod['cantidad'],
            'prodId': prod['producto__id'],
        }
        # Calcula el subtotal del carrito
        subtotal += prod['valUnit'] * prod['cantidad']
        listado.append(reg) 
    # Calcula el costo de envío según el número de productos en el carrito
    envio = 8000
    if len(listado) == 0:
        envio = 0
    # Crea un diccionario con los datos del carrito
    context = {
        'titulo': 'Productos en el carrito de compras',
        'carrito': listado,
        'subtotal': subtotal,
        'iva': int(subtotal) * 0.19,
        'envio': envio,
        'total': int(subtotal) * 1.19 + envio
    }
    # Retorna el diccionario con los datos del carrito
    return context 

def pagarCarrito(request):
    """
    Vista para procesar la compra de los productos en el carrito de compras.

    La función obtiene el contexto del carrito de compras del usuario y su información de correo electrónico. 
    Utiliza la plantilla 'productos/html_email.html' para generar el cuerpo del correo electrónico y la envía 
    a la dirección de correo electrónico del usuario. Finalmente, marca los productos del carrito como "comprados" 
    y redirige al usuario a la página de categorías.

    Args:
        request: HttpRequest object que contiene información de la solicitud HTTP.

    Returns:
        Una instancia de HttpResponse que redirige al usuario a la página de categorías.

    Raises:
        No se lanzan excepciones.
    """
    # Obtener el contexto del carrito de compras del usuario
    context = consultarCarro(request)
    regUsuario = request.user
    nombreUsuario = str(regUsuario)
    context['nombre'] = nombreUsuario
    correo = regUsuario.email
    # Módulo para envío de correo electrónico
    mail_subject = 'Factura de compra'
    body = render_to_string('productos/html_email.html', context)
    to_email = [correo]   # Lista con el o los correos de destino
    send_email = EmailMessage(mail_subject, body, to= to_email )
    send_email.content_subtype = 'html'
    send_email.send()
    # Marcar los productos del carrito como "comprados"
    listaCarrito = Carro.objects.filter(usuario= regUsuario, estado= 'activo')
    for regCarro in listaCarrito:
        regCarro.estado = 'comprado'
        regCarro.save()
    # Redireccionar al usuario a la página de categorías
    return verCategorias(request) 
