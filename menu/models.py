from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# =====================================
# MODELO PRINCIPAL DE ÓRDENES DE TRABAJO
# =====================================
class OrdenTrabajo(models.Model):

    # Estados del flujo de producción
    ESTADOS = [
        ('revision', 'Revisión'),
        ('recepcion', 'Recepción'),
        ('diseno', 'Diseño'),
        ('corte', 'Corte'),
        ('finalizado', 'Finalizado'),
        ('entregado', 'Entregado'),
    ]

    # Prioridad de la orden
    PRIORIDADES = [
        ('normal', 'Normal'),
        ('urgente', 'Urgente'),
    ]

    # Información del cliente
    empresa = models.CharField(max_length=200)
    cliente = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    descripcion = models.TextField()

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='revision'
    )

    prioridad = models.CharField(
        max_length=20,
        choices=PRIORIDADES,
        default='normal'
    )
    # Información económica
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    adelanto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # Fechas de seguimiento
    tiempo_estimado = models.IntegerField(
        help_text="Tiempo en minutos"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    fecha_inicio = models.DateTimeField(
        blank=True,
        null=True
    )

    fecha_finalizacion = models.DateTimeField(
        blank=True,
        null=True
    )
    
    # Responsable de la orden
    trabajador = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    observaciones = models.TextField(
        blank=True,
        null=True
    )

    alarma_activada = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.empresa} - {self.estado}"

    @property
    def saldo_pendiente(self):
        return self.precio - self.adelanto

    @property
    def tiempo_restante(self):

        if self.fecha_inicio:

            tiempo_transcurrido = timezone.now() - self.fecha_inicio

            minutos_transcurridos = tiempo_transcurrido.total_seconds() / 60

            restante = self.tiempo_estimado - minutos_transcurridos

            return max(0, int(restante))

        return self.tiempo_estimado



class HistorialEstado(models.Model):

    orden = models.ForeignKey(
        OrdenTrabajo,
        on_delete=models.CASCADE,
        related_name='historial'
    )

    estado = models.CharField(
        max_length=20,
        choices=OrdenTrabajo.ESTADOS
    )

    fecha_inicio = models.DateTimeField(auto_now_add=True)

    fecha_fin = models.DateTimeField(
        blank=True,
        null=True
    )

    trabajador = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.orden.empresa} - {self.estado}"