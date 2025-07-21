# inventario/admin.py
from django.contrib import admin
from .models import Cuerpo, Producto, MovimientoInventario

@admin.register(Cuerpo)
class CuerpoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cuerpo', 'cantidad', 'estado', 'ubicacion')
    list_filter = ('cuerpo', 'estado')
    search_fields = ('nombre', 'descripcion')

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'tipo_movimiento', 'cantidad', 'motivo', 'fecha_movimiento')
    list_filter = ('tipo_movimiento', 'producto__cuerpo')
