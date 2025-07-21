# inventario/forms.py
from django import forms
from .models import Producto, MovimientoInventario

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        # Excluimos 'cuerpo' porque se asigna automáticamente en la vista
        exclude = ['cuerpo']

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        # Este bucle añade la clase 'form-control' de Bootstrap a todos los campos
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            # Hacemos que el campo de fecha use el widget de fecha de HTML5
            if isinstance(field.widget, forms.DateInput):
                field.widget.input_type = 'date'

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['tipo_movimiento', 'cantidad', 'motivo']

    def __init__(self, *args, **kwargs):
        super(MovimientoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'