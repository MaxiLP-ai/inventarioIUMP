# inventario/models.py
from django.db import models
from django.utils import timezone

# Modelo para los Cuerpos o Grupos de la Iglesia
class Cuerpo(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Cuerpo")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    imagen = models.ImageField(upload_to='cuerpos/', default='cuerpos/default.png', verbose_name="Imagen del Cuerpo")

    def __str__(self):
        return self.nombre

# Modelo para los Productos del Inventario
class Producto(models.Model):
    ESTADO_CHOICES = [
        ('Nuevo', 'Nuevo'),
        ('Bueno', 'Bueno'),
        ('Usado', 'Usado'),
        ('Reparación', 'Requiere Reparación'),
    ]

    cuerpo = models.ForeignKey(Cuerpo, on_delete=models.CASCADE, related_name='productos', verbose_name="Cuerpo al que pertenece")
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    descripcion = models.TextField(verbose_name="Descripción Detallada", null=True ,default='Sin Descripción' )
    cantidad = models.PositiveIntegerField(default=0, verbose_name="Cantidad en Stock")
    imagen = models.ImageField(upload_to='productos/', default='productos/default.png', verbose_name="Imagen del Producto")
    ubicacion = models.CharField(max_length=150, blank=True, null=True, verbose_name="Ubicación Física")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Bueno', verbose_name="Estado del Producto")
    fecha_adquisicion = models.DateField(default=timezone.now, verbose_name="Fecha de Adquisición")

    def __str__(self):
        return f"{self.nombre} ({self.cantidad})"

# Modelo para registrar cada movimiento de inventario
class MovimientoInventario(models.Model):
    TIPO_MOVIMIENTO_CHOICES = [
        ('Entrada', 'Entrada'),
        ('Salida', 'Salida'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos')
    tipo_movimiento = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO_CHOICES)
    cantidad = models.PositiveIntegerField()
    motivo = models.CharField(max_length=255, verbose_name="Motivo del movimiento")
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    # podrías agregar un campo para el responsable:
    # responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.tipo_movimiento} de {self.cantidad} en {self.producto.nombre} el {self.fecha_movimiento.strftime('%d-%m-%Y')}"

