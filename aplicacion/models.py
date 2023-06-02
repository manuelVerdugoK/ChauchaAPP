from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import string
import random
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    



# HOJA DE INFORMACIÓN FINANCIERA

class HojaInformacionFinanciera(models.Model):
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_ultima_modificacion = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=User)
def crear_hoja_informacion_financiera(sender, instance, created, **kwargs):
    if created:
        HojaInformacionFinanciera.objects.create(propietario=instance)



class Ingreso(models.Model):
    TIPO_INGRESO_CHOICES = (
        ('Fijo', 'Fijo'),
        ('Esporádico', 'Esporádico'),
    )
    FUENTE_INGRESO_CHOICES = (
        ('Trabajo', 'Trabajo'),
        ('Donaciones', 'Donaciones'),
        ('Pensión', 'Pensión'),
        ('Becas y/o Beneficios', 'Becas y/o Beneficios'),
        ('Bonos', 'Bonos'),
        ('Compensación', 'Compensación'),
    )

    hoja_informacion_financiera = models.ForeignKey(HojaInformacionFinanciera, on_delete=models.CASCADE)
    tipo_ingreso = models.CharField(max_length=20, choices=TIPO_INGRESO_CHOICES)
    fuente_ingreso = models.CharField(max_length=50, choices=FUENTE_INGRESO_CHOICES)
    monto_ingreso = models.DecimalField(max_digits=10, decimal_places=2)

class Egreso(models.Model):
    TIPO_EGRESO_CHOICES = (
        ('Fijo', 'Fijo'),
        ('Esporádico', 'Esporádico'),
    )
    FUENTE_EGRESO_CHOICES = (
        ('Alimentación', 'Alimentación'),
        ('Transporte', 'Transporte'),
        ('Imprevistos', 'Imprevistos'),
        ('Salud', 'Salud'),
        ('Diversión', 'Diversión'),
        ('Educación', 'Educación'),
        ('Higiene', 'Higiene'),
        ('Vestuario', 'Vestuario'),
        ('Servicios Básicos', 'Servicios Básicos'),
        ('Servicios Tecnológicos', 'Servicios Tecnológicos'),
        ('Completos', 'Completos'),
    )

    hoja_informacion_financiera = models.ForeignKey(HojaInformacionFinanciera, on_delete=models.CASCADE)
    tipo_egreso = models.CharField(max_length=20, choices=TIPO_EGRESO_CHOICES)
    fuente_egreso = models.CharField(max_length=50, choices=FUENTE_EGRESO_CHOICES)
    monto_egreso = models.DecimalField(max_digits=10, decimal_places=2)