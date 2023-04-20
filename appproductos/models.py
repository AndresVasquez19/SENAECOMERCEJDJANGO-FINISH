from django.db import models
from appusuarios.models import Usuario

class Categoria(models.Model):
    """
    Modelo para las categorías de los productos.

    Attributes:
        descripCategoria (str): descripción de la categoría.
    """
    descripCategoria = models.CharField(max_length=100, null=False)

    def __str__(self):
        """
        Retorna la descripción de la categoría.

        Returns:
            str: descripción de la categoría.
        """
        return self.descripCategoria

    class Meta:
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías de productos'
 
class Producto(models.Model):
    """
    Modelo para los productos.

    Attributes:
        nombre (str): nombre del producto.
        descripcion (str): descripción del producto.
        precioUnitario (float): precio unitario del producto.
        unidad (str): unidad del producto.
        existencia (int): cantidad de existencia del producto.
        imgGrande (str): imagen grande del producto.
        imgPeque (str): imagen pequeña del producto.
        categoria (Categoria): categoría del producto.
    """
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.CharField(max_length=300, null=True)
    precioUnitario = models.DecimalField(max_digits=8, decimal_places=2)
    unidad = models.CharField(max_length=10, null=False) 
    existencia= models.IntegerField(null=True)
    imgGrande = models.ImageField(upload_to='productos', null=True)
    imgPeque = models.ImageField(upload_to='iconos', null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        """
        Retorna el nombre del producto.

        Returns:
            str: nombre del producto.
        """
        return self.nombre
    
class Carro(models.Model):
    # Define las opciones de estado del producto
    ESTADO_PROD =  (
        ('activo', 'activo'),
        ('comprado', 'comprado'),
        ('anulado', 'anulado'),
    )
    # Relación con el modelo Usuario
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=False)

    # Relación con el modelo Producto
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=False)

    # Cantidad de productos en el carro
    cantidad = models.IntegerField(null=False, default=1)

    # Valor unitario del producto
    valUnit = models.DecimalField(max_digits=8, decimal_places=2)

    # Estado del producto en el carro
    estado = models.CharField(max_length=20, choices=ESTADO_PROD, default='activo')
