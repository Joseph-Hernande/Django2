from django.db import models

# El modelo Usuario ya lo tienes, lo dejamos tal cual
class Usuario(models.Model):
    correo = models.EmailField(max_length=254, unique=True)
    nombre = models.CharField(max_length=100)
    clave = models.CharField(max_length=254)
    ROLES = (
        ('A', "Administrador"),
        ('D', "Desarrollador"),
        ('L', "Líder"),
    )
    rol = models.CharField(max_length=1, choices=ROLES, default='D')  # 'D' como valor predeterminado

    def __str__(self):
        return self.nombre

# Modelo Proyecto sin las fechas de inicio y fin
class Proyecto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    lider = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name="proyectos_liderados")

    def __str__(self):
        return self.nombre

# Modelo Equipo
class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="equipos")
    miembros = models.ManyToManyField(Usuario, related_name="equipos")

    def __str__(self):
        return self.nombre

# Modelo Tarea
class Tarea(models.Model):
    ESTADOS = (
        ('P', 'Pendiente'),
        ('C', 'Completada'),
        ('A', 'Asignada'),
        ('E', 'En Progreso'),
    )
    PRIORIDAD_CHOICES = [
        ('1', 'Alta'),
        ('2', 'Media'),
        ('3', 'Baja'),
    ]
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_limite = models.DateField(null=True, blank=True)
    prioridad = models.CharField(max_length=1, choices=PRIORIDAD_CHOICES, default='2')
    estado = models.CharField(max_length=1, choices=ESTADOS, default='P')
    observaciones = models.TextField(blank=True, null=True)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name="tareas")
    asignado_a = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name="tareas_asignadas")

    def __str__(self):
        return self.titulo
