from django.contrib import admin
from .models import OrdenTrabajo, HistorialEstado


@admin.register(OrdenTrabajo)
class OrdenTrabajoAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'empresa',
        'cliente',
        'estado',
        'prioridad',
        'precio',
        'fecha_creacion',
    )

    list_filter = (
        'estado',
        'prioridad',
    )

    search_fields = (
        'empresa',
        'cliente',
    )


@admin.register(HistorialEstado)
class HistorialEstadoAdmin(admin.ModelAdmin):

    list_display = (
        'orden',
        'estado',
        'fecha_inicio',
        'fecha_fin',
    )