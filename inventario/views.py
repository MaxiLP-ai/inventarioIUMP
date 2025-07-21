# inventario/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from weasyprint import HTML
from .models import Cuerpo, Producto, MovimientoInventario
from .forms import ProductoForm, MovimientoForm

# Vista para la página principal con las tarjetas de los cuerpos
def lista_cuerpos(request):
    cuerpos = Cuerpo.objects.all()
    return render(request, 'inventario/lista_cuerpos.html', {'cuerpos': cuerpos})

# Vista para el inventario de un cuerpo específico
def detalle_inventario(request, cuerpo_id):
    cuerpo = get_object_or_404(Cuerpo, id=cuerpo_id)
    productos = Producto.objects.filter(cuerpo=cuerpo)

    # Formularios para los modales
    movimiento_form = MovimientoForm() 
    producto_form = ProductoForm() # <-- NUEVO: Preparamos el form para agregar producto

    return render(request, 'inventario/detalle_inventario.html', {
        'cuerpo': cuerpo,
        'productos': productos,
        'movimiento_form': movimiento_form,
        'producto_form': producto_form, # <-- NUEVO: Lo pasamos a la plantilla
    })

# Vista para agregar un nuevo producto (AHORA USADA POR EL MODAL)
def agregar_producto(request, cuerpo_id):
    cuerpo = get_object_or_404(Cuerpo, id=cuerpo_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.cuerpo = cuerpo
            producto.save()
            # Redirigimos de vuelta a la página de inventario
            return redirect('inventario:detalle_inventario', cuerpo_id=cuerpo.id)

    # Si no es POST (o el form no es válido), simplemente redirigimos.
    # La vista de página completa para agregar ya no es la principal forma de uso.
    return redirect('inventario:detalle_inventario', cuerpo_id=cuerpo.id)


# Vista para registrar una entrada o salida de inventario
def registrar_movimiento(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.producto = producto

            if movimiento.tipo_movimiento == 'Entrada':
                producto.cantidad += movimiento.cantidad
            elif movimiento.tipo_movimiento == 'Salida':
                if producto.cantidad >= movimiento.cantidad:
                    producto.cantidad -= movimiento.cantidad
                else:
                    pass

            producto.save()
            movimiento.save()
    return redirect('inventario:detalle_inventario', cuerpo_id=producto.cuerpo.id)

# Vista para generar el reporte en PDF
def generar_pdf_inventario(request, cuerpo_id):
    cuerpo = get_object_or_404(Cuerpo, id=cuerpo_id)
    productos = Producto.objects.filter(cuerpo=cuerpo)

    context = {
        'cuerpo': cuerpo,
        'productos': productos,
        'fecha': timezone.now()
    }

    html_string = render_to_string('inventario/reporte_pdf.html', context)
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="inventario_{cuerpo.nombre.lower()}_{timezone.now().strftime("%Y-%m-%d")}.pdf"'
    return response


# ==============================================================================
# VISTA TEMPORAL PARA CREAR SUPERUSUARIO
# ==============================================================================

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
def crear_superusuario_temporal(request):
    # ¡CAMBIA ESTOS VALORES POR LOS QUE TÚ QUIERAS!
    username = "iumpadmin"
    password = "iglesiaunida1978"
    email = "renatomaxi2005@gmail.com"

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, password=password, email=email)
        return HttpResponse("<h1>Superusuario creado exitosamente.</h1><p>Por favor, elimina la URL y la vista de tu código ahora mismo.</p>")
    else:
        return HttpResponse("<h1>El superusuario ya existe.</h1>")