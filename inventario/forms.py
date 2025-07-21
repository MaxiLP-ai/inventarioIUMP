# inventario/forms.py
from django import forms
from .models import Producto, MovimientoInventario

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'cantidad', 'imagen', 'ubicacion', 'estado', 'fecha_adquisicion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'fecha_adquisicion': forms.DateInput(attrs={'type': 'date'}),
        }

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['tipo_movimiento', 'cantidad', 'motivo']