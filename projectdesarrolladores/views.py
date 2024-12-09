from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Proyecto, Tarea, Equipo, Usuario

# Vista de la página principal

#Funcion de log-in log-out
def login(request):
    if request.method == "POST":
        correo = request.POST.get("correo")
        clave = request.POST.get("clave")
        
        try:
            q = Usuario.objects.get(correo=correo, clave=clave)
            messages.success(request, "Bienvenido!!")
            
            # Asegurarse de incluir 'correo' en la sesión
            datos = {
                "id": q.id,
                "nombre": q.nombre,
                "rol": q.rol,
                "correo": q.correo  # Agregar correo
            }
            request.session["logueado"] = datos
            return redirect("index")
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario o Contraseña no válidos D:")
            return redirect("login")
    else:
        control = request.session.get("logueado", False)
        if not control:
            return render(request, "login.html")
        else:
            return redirect("index")


def logout(request):
    try:
        del request.session["logueado"]
        return redirect ("login")

    except:
        messages.error(request, "Erroe, intente de nuevo D:")
        return redirect("index")

def index(request):
    control = request.session.get("logueado", False)
    if control:
        return render(request, "index.html")
    else: 
        messages.warning(request, "Por favor inicie sesión ...")
        return redirect("login")

# Vista para ver proyectos
def ver_proyectos(request):
    control = request.session.get("logueado", False)
    if not control:
        return redirect("login")

    proyectos = Proyecto.objects.all()
    return render(request, 'proyectos.html', {'proyectos': proyectos})

# Vista para ver miembros de un equipo
def ver_miembros(request):
    control = request.session.get("logueado", False)
    if not control:
        return redirect("login")

    # Obtener los equipos y sus miembros
    equipos = Equipo.objects.all()
    return render(request, 'miembros.html', {'equipos': equipos})

def asignar_lider(request):
    if not request.session.get("logueado", False):
        return redirect("login")
    
    # Verificar si el usuario es un Administrador
    if request.session.get("logueado")["rol"] != "A":
        messages.error(request, "No tienes permiso para asignar líderes.")
        return redirect("index")

    if request.method == 'POST':
        proyecto_id = request.POST['proyecto']
        lider_id = request.POST['lider']
        proyecto = Proyecto.objects.get(id=proyecto_id)
        lider = Usuario.objects.get(id=lider_id)
        proyecto.lider = lider
        proyecto.save()
        messages.success(request, "Líder asignado exitosamente.")
        return redirect('ver_proyectos')
    
    proyectos = Proyecto.objects.all()
    lideres = Usuario.objects.filter(rol='L')  # Suponiendo que los Líderes tienen rol 'L'
    return render(request, 'registro_lider.html', {'proyectos': proyectos, 'lideres': lideres})

def crear_equipo(request):
    if not request.session.get("logueado", False):
        return redirect("login")
    
    if request.session.get("logueado")["rol"] != "L":
        messages.error(request, "No tienes permiso para crear equipos.")
        return redirect("index")

    # Obtener el id del líder actual desde la sesión
    lider_id = request.session.get("logueado")["id"]

    # Filtrar los proyectos que el líder tiene asignados
    proyecto_asignado = Proyecto.objects.filter(lider__id=lider_id).first()

    # Si no hay proyectos asignados
    if not proyecto_asignado:
        messages.error(request, "No tienes proyectos asignados.")
        return redirect("index")
    
    # Obtener usuarios con rol 'Desarrollador'
    miembros = Usuario.objects.filter(rol='D')

    if request.method == 'POST':
        # Crear un equipo
        nombre_equipo = request.POST.get('nombre_equipo')
        proyecto_id = request.POST.get('proyecto')
        equipo = Equipo.objects.create(
            nombre=nombre_equipo,
            proyecto_id=proyecto_id
        )
        
        # Agregar miembros seleccionados al equipo (permitiendo múltiples selecciones)
        miembros_ids = request.POST.getlist('miembros')  # Esto obtiene los IDs de los miembros seleccionados
        for miembro_id in miembros_ids:
            miembro = Usuario.objects.get(id=miembro_id)
            equipo.miembros.add(miembro)
        
        equipo.save()
        
        messages.success(request, "Equipo creado exitosamente.")
        return redirect("crear_equipo")

    return render(request, 'crear_equipo.html', {
        'proyecto_asignado': proyecto_asignado,
        'miembros': miembros,
    })

def crear_proyecto(request):
    if not request.session.get("logueado", False):
        return redirect("login")
    
    # Verificar si el usuario es un Administrador
    if request.session.get("logueado")["rol"] != "A":
        messages.error(request, "No tienes permiso para crear proyectos.")
        return redirect("index")

    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        lider_id = request.POST['lider']
        
        # Obtener al líder desde el ID seleccionado
        lider = Usuario.objects.get(id=lider_id)

        # Crear el proyecto con el líder asignado
        Proyecto.objects.create(nombre=nombre, descripcion=descripcion, lider=lider)
        messages.success(request, "Proyecto creado exitosamente.")
        return redirect('ver_proyectos')

    # Obtener los usuarios con el rol de 'L' (Líder)
    lideres = Usuario.objects.filter(rol='L')

    return render(request, 'crear_proyecto.html', {'lideres': lideres})

def ver_equipo(request):
    # Asegurarse de que el usuario tiene permisos
    if not request.session.get("logueado", False):
        return redirect("login")
    
    if request.session.get("logueado")["rol"] != "L":
        messages.error(request, "No tienes permiso para ver equipos.")
        return redirect("index")
    
    # Obtener el equipo creado (por ejemplo, el último equipo creado o por alguna lógica específica)
    equipo = Equipo.objects.last()  # O usa alguna lógica para obtener el equipo que creaste
    
    return render(request, 'ver_equipo.html', {'equipo': equipo})

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario
from django.contrib.auth.hashers import make_password

def registrar_desarrolladores(request):
    if not request.session.get("logueado", False):
        return redirect("login")
    
    if request.session.get("logueado")["rol"] != "L":
        messages.error(request, "No tienes permiso para registrar usuarios.")
        return redirect("index")

    if request.method == 'POST':
        correo = request.POST['correo']
        nombre = request.POST['nombre']
        clave = request.POST['clave']

        # Verificar si el correo ya está registrado
        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, "Este correo ya está registrado.")
        else:
            # Crear el nuevo usuario
            usuario = Usuario(
                correo=correo,
                nombre=nombre,
                clave=make_password(clave),  # Encriptamos la contraseña
                rol='D'  # Asignar rol de Desarrollador
            )
            usuario.save()

            messages.success(request, "Usuario registrado exitosamente.")
            return redirect('registrar_desarrolladores')  # Redirigir a la página de registro de usuario

    return render(request, 'registrar_desarrolladores.html')

def crear_tarea(request):
    if not request.session.get("logueado", False):
        return redirect("login")
    
    if request.session.get("logueado")["rol"] != "L":
        messages.error(request, "No tienes permiso para crear tareas.")
        return redirect("index")

    # Obtener el id del líder actual desde la sesión
    lider_id = request.session.get("logueado")["id"]

    # Filtrar los proyectos que el líder tiene asignados
    proyectos = Proyecto.objects.filter(lider__id=lider_id)

    if request.method == 'POST':
        # Obtener los datos del formulario
        proyecto_id = request.POST.get('proyecto')
        equipo_id = request.POST.get('equipo')
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        fecha_limite = request.POST.get('fecha_limite')
        prioridad = request.POST.get('prioridad')
        asignado_a_id = request.POST.get('asignado_a')

        # Obtener los objetos de Proyecto, Equipo y Usuario asignado
        proyecto = Proyecto.objects.get(id=proyecto_id)
        equipo = Equipo.objects.get(id=equipo_id)
        
        # Si no se selecciona un usuario, asignado_a será None (Aún no asignado)
        asignado_a = Usuario.objects.get(id=asignado_a_id) if asignado_a_id != '0' else None

        # Crear la tarea
        tarea = Tarea(
            titulo=titulo,
            descripcion=descripcion,
            fecha_limite=fecha_limite,
            prioridad=prioridad,
            estado='P',  # Estado inicial de la tarea
            equipo=equipo,
            asignado_a=asignado_a
        )
        tarea.save()
        
        messages.success(request, "Tarea creada exitosamente.")
        return redirect('crear_tarea')  # Redirigir a la página de creación de tarea

    # Obtener todos los equipos de los proyectos del líder
    equipos = Equipo.objects.filter(proyecto__in=proyectos)
    
    # Inicialmente no filtramos usuarios aquí, sino que se filtrarán en función del equipo
    usuarios = []

    return render(request, 'crear_tarea.html', {
        'proyectos': proyectos,
        'equipos': equipos,
        'usuarios': usuarios,  # Lista vacía al inicio
    })

def obtener_equipos_por_proyecto(request, proyecto_id):
    equipos = Equipo.objects.filter(proyecto_id=proyecto_id)
    equipos_data = [{'id': equipo.id, 'nombre': equipo.nombre} for equipo in equipos]
    return JsonResponse({'equipos': equipos_data})

def obtener_miembros_por_equipo(request, equipo_id):
    equipo = Equipo.objects.get(id=equipo_id)
    miembros = equipo.miembros.filter(rol='D')  # Filtrar solo desarrolladores
    miembros_data = [{'id': miembro.id, 'nombre': miembro.nombre} for miembro in miembros]
    return JsonResponse({'miembros': miembros_data})

def eliminar_tarea(request, tarea_id):
    # Verificar si el usuario está logueado
    control = request.session.get("logueado", False)
    if not control:
        return redirect("login")

    # Verificar que el usuario es un líder
    if request.session['logueado']['rol'] != 'L':
        messages.error(request, "No tienes permisos para eliminar tareas.")
        return redirect('index')

    tarea = Tarea.objects.get(id=tarea_id)
    
    # Verificar si la tarea está asignada
    if tarea.asignado_a:
        tarea.estado = 'D'  # Desactivada
        tarea.save()
        messages.success(request, "La tarea ha sido desactivada.")
    else:
        tarea.delete()
        messages.success(request, "Tarea eliminada exitosamente.")

    return redirect('ver_tareas')

def registrar_lid_adm(request):
    if not request.session.get("logueado", False):
        return redirect("login")
    
    if request.session.get("logueado")["rol"] != "A":
        messages.error(request, "No tienes permiso para registrar usuarios.")
        return redirect("index")

    if request.method == 'POST':
        correo = request.POST['correo']
        nombre = request.POST['nombre']
        clave = request.POST['clave']
        rol = request.POST['rol']  # Obtener el rol seleccionado

        # Verificar si el correo ya está registrado
        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, "Este correo ya está registrado.")
        else:
            # Crear el nuevo usuario con el rol seleccionado
            usuario = Usuario(
                correo=correo,
                nombre=nombre,
                clave=make_password(clave),  # Encriptamos la contraseña
                rol=rol  # Asignar el rol seleccionado
            )
            usuario.save()

            messages.success(request, "Usuario registrado exitosamente.")
            return redirect('registrar_lid_adm')  # Redirigir a la página de registro de usuario

    return render(request, 'registrar_lid_adm.html')

def listar_usuarios(request):
    if not request.session.get("logueado", False) or request.session["logueado"]["rol"] != "A":
        messages.error(request, "No tienes permisos para ver esta página.")
        return redirect('index')

    usuarios = Usuario.objects.all()
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})

# Vista para eliminar usuario
def eliminar_usuario(request, usuario_id):
    if request.session.get("logueado", False) and request.session["logueado"]["rol"] == "A":
        usuario = get_object_or_404(Usuario, id=usuario_id)
        
        if usuario.id != 1:  # No permitir eliminar al usuario con id=1 (Administrador)
            usuario.delete()
            messages.success(request, f"Usuario {usuario.nombre} eliminado correctamente.")
        else:
            messages.error(request, "No puedes eliminar al administrador principal.")
        
        return redirect('listar_usuarios')
    else:
        messages.error(request, "No tienes permisos para realizar esta acción.")
        return redirect('index')

# Vista para cambiar rol
def cambiar_rol(request, usuario_id):
    # Verificar si el usuario está logueado y tiene rol "A"
    if not request.session.get("logueado", {}).get("rol") == "A":
        messages.error(request, "No tienes permisos para realizar esta acción.")
        return redirect('index')

    usuario = get_object_or_404(Usuario, id=usuario_id)

    # Restringir cambios al usuario principal con id=1
    if usuario.id == 1:
        messages.error(request, "No puedes cambiar el rol del usuario principal (Administrador).")
        return redirect('listar_usuarios')

    if request.method == 'POST':
        # Lógica para cambiar el rol entre Líder (L) y Desarrollador (D)
        if usuario.rol == 'L':
            usuario.rol = 'D'  # Cambiar a Desarrollador
        elif usuario.rol == 'D':
            usuario.rol = 'L'  # Cambiar a Líder
        usuario.save()
        messages.success(request, f"Rol de {usuario.nombre} cambiado a {usuario.get_rol_display()}.")
        return redirect('listar_usuarios')

    # Redirigir en caso de acceso no permitido
    messages.error(request, "Método no permitido.")
    return redirect('listar_usuarios')
    
def listar_tareas(request):
    if not request.session.get("logueado", False):
        return redirect("login")
    
    if request.session.get("logueado")["rol"] != "L":
        messages.error(request, "No tienes permiso para ver las tareas.")
        return redirect("index")

    # Obtener el id del líder actual desde la sesión
    lider_id = request.session.get("logueado")["id"]

    # Filtrar tareas relacionadas a los proyectos del líder
    tareas = Tarea.objects.filter(equipo__proyecto__lider__id=lider_id)

    return render(request, 'listar_tareas.html', {'tareas': tareas})

def editar_tarea(request, tarea_id):
    if not request.session.get("logueado", False):
        return redirect("login")
    
    if request.session.get("logueado")["rol"] != "L":
        messages.error(request, "No tienes permiso para editar tareas.")
        return redirect("index")

    tarea = Tarea.objects.get(id=tarea_id)

    # Verificar si el líder tiene acceso al proyecto/equipo asociado
    if tarea.equipo.proyecto.lider.id != request.session.get("logueado")["id"]:
        messages.error(request, "No tienes acceso a esta tarea.")
        return redirect("listar_tareas")

    if request.method == 'POST':
        tarea.estado = request.POST.get('estado')
        tarea.observaciones = request.POST.get('observaciones')
        asignado_a_id = request.POST.get('asignado_a')
        if asignado_a_id != '0':
            tarea.asignado_a = Usuario.objects.get(id=asignado_a_id)
        else:
            tarea.asignado_a = None
        tarea.save()

        messages.success(request, "Tarea actualizada exitosamente.")
        return redirect('listar_tareas')

    return render(request, 'editar_tarea.html', {'tarea': tarea})


def eliminar_tarea(request, tarea_id):
    if not request.session.get("logueado", False):
        return redirect("login")
    
    if request.session.get("logueado")["rol"] != "L":
        messages.error(request, "No tienes permiso para eliminar tareas.")
        return redirect("index")

    tarea = Tarea.objects.get(id=tarea_id)

    # Verificar si el líder tiene acceso al proyecto/equipo asociado
    if tarea.equipo.proyecto.lider.id != request.session.get("logueado")["id"]:
        messages.error(request, "No tienes acceso a esta tarea.")
        return redirect("listar_tareas")

    # Solo eliminar si no tiene desarrollador asignado
    if tarea.asignado_a:
        messages.error(request, "No puedes eliminar esta tarea porque ya está asignada.")
        return redirect("listar_tareas")

    tarea.delete()
    messages.success(request, "Tarea eliminada exitosamente.")
    return redirect("listar_tareas")

def listar_tareas_equipo(request):
    # Verificar si el usuario está logueado
    if not request.session.get("logueado", False):
        return redirect("login")

    # Verificar que el usuario es un desarrollador
    if request.session["logueado"]["rol"] != "D":
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect("index")

    # Obtener el ID del usuario actual desde la sesión
    usuario_id = request.session["logueado"]["id"]

    # Obtener los equipos a los que pertenece el usuario y las tareas relacionadas
    equipos = Equipo.objects.filter(miembros__id=usuario_id)
    tareas = Tarea.objects.filter(equipo__in=equipos)

    if request.method == "POST":
        # Obtener el ID de la tarea desde el formulario
        tarea_id = request.POST.get("tarea_id")
        tarea = Tarea.objects.get(id=tarea_id)

        # Verificar que la tarea pertenezca a los equipos del usuario
        if tarea.equipo not in equipos:
            messages.error(request, "No tienes permiso para editar esta tarea.")
            return redirect("listar_tareas_equipo")

        # Actualizar los campos de la tarea
        tarea.estado = request.POST.get("estado", tarea.estado)
        tarea.observaciones = request.POST.get("observaciones", tarea.observaciones)

        # Obtener el ID del miembro asignado
        asignado_a_id = request.POST.get("asignado_a")
        
        # Si no se asigna a nadie (valor vacío o '0'), se establece a None
        if asignado_a_id == "0" or asignado_a_id == "":
            tarea.asignado_a = None
        else:
            tarea.asignado_a_id = asignado_a_id  # Asignar el miembro seleccionado
        
        tarea.save()

        messages.success(request, "Tarea actualizada correctamente.")
        return redirect("listar_tareas_equipo")

    return render(request, "listar_tareas_equipo.html", {
        "tareas": tareas,
    })

def listar_tareas(request):
    if not request.session.get("logueado", False):
        return redirect("login")

    # Verificar el rol del usuario
    if request.session.get("logueado")["rol"] != "L":
        messages.error(request, "No tienes permiso para ver las tareas.")
        return redirect("index")

    # Obtener el id del líder actual desde la sesión
    lider_id = request.session.get("logueado")["id"]

    # Filtrar tareas relacionadas a los proyectos del líder
    tareas = Tarea.objects.filter(equipo__proyecto__lider__id=lider_id)

    return render(request, 'listar_tareas.html', {'tareas': tareas})

def mis_tareas(request):
    if not request.session.get("logueado", False):
        return redirect("login")
    
    usuario = request.session.get("logueado")
    tareas = Tarea.objects.filter(asignado_a__id=usuario["id"])

    if request.method == 'POST':
        tarea_id = request.POST.get('tarea_id')
        tarea = Tarea.objects.get(id=tarea_id)

        # Solo el desarrollador puede cambiar el estado, las observaciones y la asignación
        if tarea.asignado_a.id == usuario["id"]:
            tarea.estado = request.POST.get('estado')
            tarea.observaciones = request.POST.get('observaciones')
            asignado_a_id = request.POST.get('asignado_a')
            if asignado_a_id != '0':
                tarea.asignado_a = Usuario.objects.get(id=asignado_a_id)
            else:
                tarea.asignado_a = None
            tarea.save()
            messages.success(request, "Tarea actualizada exitosamente.")
            return redirect('mis_tareas')

    return render(request, 'listar_tareas_desarrollador.html', {'tareas': tareas})






