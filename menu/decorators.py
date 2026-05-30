from django.shortcuts import redirect


# =====================================
# SOLO ADMINISTRADORES
# =====================================
def solo_admin(view_func):

    def wrapper(request, *args, **kwargs):

        if request.user.groups.filter(
            name='Administrador'
        ).exists():

            return view_func(
                request,
                *args,
                **kwargs
            )

        return redirect('login')

    return wrapper


# =====================================
# TRABAJADORES Y ADMINISTRADORES
# =====================================
def solo_trabajador(view_func):

    def wrapper(request, *args, **kwargs):

        if (

            request.user.groups.filter(
                name='Trabajador'
            ).exists()

            or

            request.user.groups.filter(
                name='Administrador'
            ).exists()

        ):

            return view_func(
                request,
                *args,
                **kwargs
            )

        return redirect('login')

    return wrapper


# =====================================
# KANBAN Y PRODUCCIÓN
# =====================================
def admin_o_trabajador(view_func):

    def wrapper(request, *args, **kwargs):

        if (

            request.user.groups.filter(
                name='Administrador'
            ).exists()

            or

            request.user.groups.filter(
                name='Trabajador'
            ).exists()

        ):

            return view_func(
                request,
                *args,
                **kwargs
            )

        return redirect('login')

    return wrapper