# inventario/urls.py
from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.lista_cuerpos, name='lista_cuerpos'),
    path('cuerpo/<int:cuerpo_id>/', views.detalle_inventario, name='detalle_inventario'),
    path('cuerpo/<int:cuerpo_id>/agregar/', views.agregar_producto, name='agregar_producto'),
    path('producto/<int:producto_id>/movimiento/', views.registrar_movimiento, name='registrar_movimiento'),
    path('cuerpo/<int:cuerpo_id>/pdf/', views.generar_pdf_inventario, name='generar_pdf'),
]