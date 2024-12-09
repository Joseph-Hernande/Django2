from django.urls import path
from . import views

urlpatterns = [
    # ========================================
    # Rutas principales
    # ========================================
    path("", views.index, name="index"),
    
    # Rutas de autenticación
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    
    # ========================================
    # Gestión de Proyectos
    # ========================================
    path("proyectos/", views.ver_proyectos, name="ver_proyectos"),
    path("crear-proyecto/", views.crear_proyecto, name="crear_proyecto"),

    # ========================================
    # Gestión de Equipos
    # ========================================
    path("crear-equipo/", views.crear_equipo, name="crear_equipo"),
    path("ver-equipo/", views.ver_equipo, name="ver_equipo"),

    # ========================================
    # Gestión de Miembros
    # ========================================
    path("miembros/", views.ver_miembros, name="ver_miembros"),
    path("registrar-desarrolladores/", views.registrar_desarrolladores, name="registrar_desarrolladores"),
    path("registrar-lid-adm/", views.registrar_lid_adm, name="registrar_lid_adm"),

    # ========================================
    # Gestión de Usuarios
    # ========================================
    path("usuarios/", views.listar_usuarios, name="listar_usuarios"),
    path("eliminar_usuario/<int:usuario_id>/", views.eliminar_usuario, name="eliminar_usuario"),
    path("cambiar_rol/<int:usuario_id>/", views.cambiar_rol, name="cambiar_rol"),

    # ========================================
    # Gestión de Líderes y Administradores
    # ========================================
    path("registro-lider/", views.asignar_lider, name="registro_lider"),

    # ========================================
    # Gestión de Tareas
    # ========================================
    path("crear_tarea/", views.crear_tarea, name="crear_tarea"),
    path("tareas/", views.listar_tareas, name="listar_tareas"),
    path("tareas/editar/<int:tarea_id>/", views.editar_tarea, name="editar_tarea"),
    path("tareas/eliminar/<int:tarea_id>/", views.eliminar_tarea, name="eliminar_tarea"),
    path("tareas-equipo/", views.listar_tareas_equipo, name="listar_tareas_equipo"),
    
    # Rutas específicas de tareas y equipos
    path("equipos-de-proyecto/<int:proyecto_id>/", views.obtener_equipos_por_proyecto, name="equipos_por_proyecto"),
    path("miembros-de-equipo/<int:equipo_id>/", views.obtener_miembros_por_equipo, name="miembros_por_equipo"),

    # Rutas de tareas para desarrolladores
    path("mis_tareas/", views.mis_tareas, name="mis_tareas"),
]
