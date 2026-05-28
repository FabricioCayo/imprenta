from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.redireccion_dashboard,
        name='inicio'
    ),

    path(
        'admin-dashboard/',
        views.dashboard_admin,
        name='dashboard_admin'
    ),

    path(
        'trabajador/',
        views.dashboard_trabajador,
        name='dashboard_trabajador'
    ),

    path(
        'cliente/',
        views.dashboard_cliente,
        name='dashboard_cliente'
    ),

    path(
        'crear/',
        views.crear_orden,
        name='crear_orden'
    ),

    path(
        'editar/<int:id>/',
        views.editar_orden,
        name='editar_orden'
    ),

    path(
        'eliminar/<int:id>/',
        views.eliminar_orden,
        name='eliminar_orden'
    ),

    path(
        'cambiar-estado/<int:id>/',
        views.cambiar_estado,
        name='cambiar_estado'
    ),

    path(
        'usuarios/',
        views.lista_usuarios,
        name='lista_usuarios'
    ),

    path(
        'usuarios/crear/',
        views.crear_usuario,
        name='crear_usuario'
    ),

    path(
        'usuarios/editar/<int:id>/',
        views.editar_usuario,
        name='editar_usuario'
    ),

    path(
        'usuarios/eliminar/<int:id>/',
        views.eliminar_usuario,
        name='eliminar_usuario'
    ),

    path(
        'kanban/',
        views.kanban,
        name='kanban'
    ),
    
    path(
        'actualizar-cliente/',
        views.actualizar_cliente,
        name='actualizar_cliente'
    ),
]