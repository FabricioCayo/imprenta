from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import OrdenTrabajo
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from .forms import OrdenTrabajoForm
from .models import HistorialEstado

from .decorators import solo_admin, solo_trabajador

from django.db.models import Sum, Count
from django.utils.timezone import now

from django.contrib.auth.models import User, Group
from .forms import UsuarioForm

from .decorators import (
    solo_admin,
    solo_trabajador,
    admin_o_trabajador
)


from django.views.decorators.cache import never_cache

@login_required
def redireccion_dashboard(request):

    if request.user.groups.filter(
        name='Administrador'
    ).exists():

        return redirect('dashboard_admin')

    elif request.user.groups.filter(
        name='Trabajador'
    ).exists():

        return redirect('dashboard_trabajador')

    else:

        return redirect('dashboard_cliente')


@login_required
@solo_admin
def dashboard_admin(request):

    ordenes = OrdenTrabajo.objects.all()

    buscar = request.GET.get('buscar')

    if buscar:

        ordenes = ordenes.filter(
            empresa__icontains=buscar
        ) | ordenes.filter(
            cliente__icontains=buscar
        )


    hoy = now().date()

    pedidos_hoy = OrdenTrabajo.objects.filter(
        fecha_creacion__date=hoy
    ).count()

    completados_hoy = OrdenTrabajo.objects.filter(
        estado='finalizado',
        fecha_finalizacion__date=hoy
    ).count()

    pendientes = OrdenTrabajo.objects.exclude(
        estado='entregado'
    ).count()

    urgentes = OrdenTrabajo.objects.filter(
        prioridad='urgente'
    ).count()

    ingresos_hoy = OrdenTrabajo.objects.filter(
        fecha_creacion__date=hoy
    ).aggregate(
        total=Sum('precio')
    )['total'] or 0


    # GRÁFICO ESTADOS
    estados = OrdenTrabajo.objects.values(
        'estado'
    ).annotate(
        total=Count('id')
    )

    labels_estados = []
    data_estados = []

    for estado in estados:

        labels_estados.append(
            estado['estado']
        )

        data_estados.append(
            estado['total']
        )
    context = {

        'ordenes': ordenes,

        'pedidos_hoy': pedidos_hoy,

        'completados_hoy': completados_hoy,

        'pendientes': pendientes,

        'urgentes': urgentes,

        'ingresos_hoy': ingresos_hoy,

        'labels_estados': labels_estados,

        'data_estados': data_estados,
    }

    return render(
        request,
        'menu/admin_dashboard.html',
        context
    )


@login_required
@solo_trabajador
def dashboard_trabajador(request):

    ordenes = OrdenTrabajo.objects.all()

    context = {
        'ordenes': ordenes
    }

    return render(
        request,
        'menu/trabajador_dashboard.html',
        context
    )


def dashboard_cliente(request):

    ordenes = OrdenTrabajo.objects.exclude(
        estado='entregado'
    ).filter(
        archivado=False
    )
    context = {
        'ordenes': ordenes
    }

    return render(
        request,
        'menu/cliente_dashboard.html',
        context
    )

@login_required
@solo_admin
def crear_orden(request):

    if request.method == 'POST':

        form = OrdenTrabajoForm(request.POST)

        if form.is_valid():

            orden = form.save(commit=False)

            if orden.estado != 'revision':
                orden.fecha_inicio = timezone.now()

            orden.save()

            HistorialEstado.objects.create(
                orden=orden,
                estado=orden.estado,
                trabajador=orden.trabajador
            )

            messages.success(
                request,
                'Orden creada correctamente'
            )

            return redirect('dashboard_admin')

    else:

        form = OrdenTrabajoForm()

    context = {
        'form': form
    }

    return render(
        request,
        'menu/orden_form.html',
        context
    )

@login_required
@solo_admin
def editar_orden(request, id):

    orden = get_object_or_404(
        OrdenTrabajo,
        id=id
    )

    estado_anterior = orden.estado

    if request.method == 'POST':

        form = OrdenTrabajoForm(
            request.POST,
            instance=orden
        )

        if form.is_valid():

            orden = form.save()

            if estado_anterior != orden.estado:

                HistorialEstado.objects.create(
                    orden=orden,
                    estado=orden.estado,
                    trabajador=orden.trabajador
                )

                if orden.estado == 'recepcion' and not orden.fecha_inicio:

                    orden.fecha_inicio = timezone.now()

                if orden.estado == 'finalizado':

                    orden.fecha_finalizacion = timezone.now()

                if orden.estado == 'entregado':

                    orden.archivado = True

                orden.save()

            messages.success(
                request,
                'Orden actualizada'
            )

            return redirect('dashboard_admin')

    else:

        form = OrdenTrabajoForm(instance=orden)

    context = {
        'form': form
    }

    return render(
        request,
        'menu/orden_form.html',
        context
    )



@login_required
@solo_admin
def eliminar_orden(request, id):

    orden = get_object_or_404(
        OrdenTrabajo,
        id=id
    )

    orden.delete()

    messages.success(
        request,
        'Orden eliminada'
    )

    return redirect('dashboard_admin')

from django.utils import timezone


@login_required
@solo_trabajador
def cambiar_estado(request, id):

    orden = get_object_or_404(
        OrdenTrabajo,
        id=id
    )

    estados = [

        'revision',
        'recepcion',
        'diseno',
        'corte',
        'finalizado',
        'entregado'
    ]

    indice = estados.index(
        orden.estado
    )

    if indice < len(estados) - 1:

        nuevo_estado = estados[indice + 1]

        orden.estado = nuevo_estado

        # INICIAR TEMPORIZADOR
        if (
            nuevo_estado == 'recepcion'
            and not orden.fecha_inicio
        ):

            orden.fecha_inicio = timezone.now()

        # FINALIZAR ORDEN
        if nuevo_estado == 'finalizado':

            orden.fecha_finalizacion = timezone.now()

        if nuevo_estado == 'entregado':

            orden.archivado = True

        orden.save()

        # HISTORIAL
        HistorialEstado.objects.create(

            orden=orden,

            estado=nuevo_estado,

            trabajador=request.user
        )

        if nuevo_estado == 'entregado':

            messages.success(
                request,
                'Orden marcada como entregada'
            )

    return redirect('kanban')

@login_required
@solo_admin
def lista_usuarios(request):

    usuarios = User.objects.all()

    context = {
        'usuarios': usuarios
    }

    return render(
        request,
        'menu/lista_usuarios.html',
        context
    )

@login_required
@solo_admin
def crear_usuario(request):

    if request.method == 'POST':

        form = UsuarioForm(request.POST)

        if form.is_valid():

            usuario = form.save()

            grupo = form.cleaned_data['grupo']

            usuario.groups.clear()

            usuario.groups.add(grupo)

            messages.success(
                request,
                'Usuario creado correctamente'
            )

            return redirect('lista_usuarios')

    else:

        form = UsuarioForm()

    context = {
        'form': form
    }

    return render(
        request,
        'menu/usuario_form.html',
        context
    )

@login_required
@solo_admin
def editar_usuario(request, id):

    usuario = get_object_or_404(
        User,
        id=id
    )

    if request.method == 'POST':

        grupo_id = request.POST.get('grupo')

        usuario.username = request.POST.get('username')

        usuario.email = request.POST.get('email')

        usuario.save()

        usuario.groups.clear()

        usuario.groups.add(grupo_id)

        messages.success(
            request,
            'Usuario actualizado'
        )

        return redirect('lista_usuarios')

    grupos = Group.objects.all()

    context = {
        'usuario': usuario,
        'grupos': grupos
    }

    return render(
        request,
        'menu/editar_usuario.html',
        context
    )

@login_required
@solo_admin
def eliminar_usuario(request, id):

    usuario = get_object_or_404(
        User,
        id=id
    )

    usuario.delete()

    messages.success(
        request,
        'Usuario eliminado'
    )

    return redirect('lista_usuarios')


@login_required
@admin_o_trabajador
def kanban(request):

    ordenes_activas = OrdenTrabajo.objects.filter(
        archivado=False
    ).exclude(
        estado='entregado'
    )

    revision = ordenes_activas.filter(
        estado='revision'
    )

    recepcion = ordenes_activas.filter(
        estado='recepcion'
    )

    diseno = ordenes_activas.filter(
        estado='diseno'
    )

    corte = ordenes_activas.filter(
        estado='corte'
    )

    finalizado = ordenes_activas.filter(
        estado='finalizado'
    )
    

    context = {

        'revision': revision,
        'recepcion': recepcion,
        'diseno': diseno,
        'corte': corte,
        'finalizado': finalizado,
    }

    return render(
        request,
        'menu/kanban.html',
        context
    )


@never_cache
def actualizar_cliente(request):

    ordenes = OrdenTrabajo.objects.exclude(
        estado='entregado'
    ).filter(
        archivado=False
    )
    return render(

        request,

        'menu/partials/ordenes_cliente.html',

        {
            'ordenes': ordenes
        }
    )