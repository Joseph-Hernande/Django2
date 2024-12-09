from django.contrib import admin
from .models import Usuario, Proyecto, Equipo, Tarea

# Registro del modelo Usuario
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ["id", "nombre", "correo", "rol"]
    search_fields = ["nombre", "correo"]
    list_filter = ["rol"]

admin.site.register(Usuario, UsuarioAdmin)

# Registro del modelo Proyecto sin las fechas de inicio y fin
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "descripcion", "lider"]
    search_fields = ["nombre", "descripcion"]
    list_filter = ["lider"]

admin.site.register(Proyecto, ProyectoAdmin)

# Registro del modelo Equipo con miembros del equipo
class EquipoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "proyecto", "miembros_equipo"]
    search_fields = ["nombre", "proyecto__nombre"]
    list_filter = ["proyecto"]

    # Método para obtener los miembros del equipo
    def miembros_equipo(self, obj):
        # Accede a los miembros del equipo (suponiendo que "miembros" es una relación a Usuario)
        miembros = obj.miembros.all()
        # Retorna los nombres de los miembros, separados por coma
        return ", ".join([miembro.nombre for miembro in miembros])
    miembros_equipo.short_description = "Miembros del equipo"

admin.site.register(Equipo, EquipoAdmin)

# Registro del modelo Tarea
class TareaAdmin(admin.ModelAdmin):
    list_display = ["titulo", "fecha_limite", "prioridad", "estado", "equipo", "asignado_a"]
    search_fields = ["titulo", "descripcion"]
    list_filter = ["estado", "equipo", "asignado_a"]

admin.site.register(Tarea, TareaAdmin)
