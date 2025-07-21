# inventario/forms.py
from django import forms
from .models import Producto, MovimientoInventario

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        exclude = ['cuerpo']
        # CORRECCIÓN: Especificamos el widget y el formato para el campo de fecha.
        widgets = {
            'fecha_adquisicion': forms.DateInput(
                format='%Y-%m-%d', # Formato AAAA-MM-DD
                attrs={'type': 'date'} # Asegura que sea un campo de fecha HTML5
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        # Este bucle añade la clase 'form-control' de Bootstrap a todos los campos.
        for field_name, field in self.fields.items():
            field.widget.attrs.setdefault('class', 'form-control')

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['tipo_movimiento', 'cantidad', 'motivo']

    def __init__(self, *args, **kwargs):
        super(MovimientoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'