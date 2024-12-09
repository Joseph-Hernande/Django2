# Generated by Django 5.1.3 on 2024-11-10 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('clave', models.CharField(max_length=254)),
                ('rol', models.CharField(choices=[('A', 'Administrador'), ('B', 'Desarrollador')], default='E', max_length=1)),
            ],
        ),
    ]
