from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import string
import random

def generar_codigo_invitacion():
    # Generar un código de invitación único de 10 caracteres
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(10))
    return code

class Espacio(models.Model):
    id = models.AutoField(primary_key=True)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)
    usuarios = models.ManyToManyField(User, related_name='espacios')
    codigo_invitacion = models.CharField(max_length=10, unique=True, default=generar_codigo_invitacion)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    nombre = models.CharField(max_length=255, default='Mi Espacio')
    descripcion = models.TextField(default='Espacio de trabajo personal')

    def save(self, *args, **kwargs):
        # Agregar automáticamente al usuario propietario a la lista de usuarios
        if not self.pk:
            super().save(*args, **kwargs)  # Guardar el objeto antes de agregar al propietario
            self.usuarios.add(self.propietario)
        else:
            super().save(*args, **kwargs)

        # Actualizar la fecha de creación al guardar el espacio
        if not self.id:
            self.fecha_creacion = timezone.now()

        return super().save(*args, **kwargs)