# Generated by Django 5.1.3 on 2024-11-15 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectdesarrolladores', '0006_alter_usuario_rol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarea',
            name='prioridad',
            field=models.CharField(choices=[('1', 'Alta'), ('2', 'Media'), ('3', 'Baja')], default='2', max_length=1),
        ),
    ]
