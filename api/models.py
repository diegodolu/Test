from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
import uuid

class Rol(models.Model):
    id = models.AutoField(primary_key=True)
    categoria = models.CharField(max_length=50)

class UsuarioManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('El usuario debe tener un nombre de usuario válido.')

        user = self.model(
            username=username,
            **extra_fields
        )

         # Encriptar la contraseña usando make_password
        if password is not None:
            user.password = make_password(password)
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(max_length=100, unique=True, default='')
    idRol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    idRaspberry = models.ManyToManyField('Raspberry')

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nombre', 'idRol']

class PasswordResetToken(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Raspberry(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=10)
    ruta = models.CharField(max_length=100, blank=True, default='')
    area = models.FloatField()
    latitud = models.FloatField()
    longitud = models.FloatField()
    bateria = models.FloatField()

class Esp32Humedad(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=10)
    bateria = models.FloatField()
    latitud = models.FloatField()
    longitud = models.FloatField()
    idRaspberry = models.ForeignKey(Raspberry, on_delete=models.CASCADE)

class Esp32Control(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=10)
    area = models.FloatField()
    bateria = models.FloatField()
    descarga = models.FloatField()
    latitud = models.FloatField()
    longitud = models.FloatField()
    idRaspberry = models.ForeignKey(Raspberry, on_delete=models.CASCADE)
    
class LecturaRaspberry(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField()
    humedad_ambiente = models.FloatField()
    temperatura_ambiente = models.FloatField()
    radiacion_solar = models.FloatField()
    presion_atmosferica = models.FloatField()
    velocidad_viento = models.FloatField()
    et0 = models.FloatField()
    ruta = models.CharField(max_length=100)
    idRaspberry = models.ForeignKey(Raspberry, on_delete=models.CASCADE)

class LecturaEsp32(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField()
    humedad_suelo = models.FloatField()
    idEsp32 = models.ForeignKey(Esp32Humedad, on_delete=models.CASCADE)

class Programa(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField()
    semana = models.IntegerField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    kc = models.FloatField()
    volumen_ha = models.FloatField()
    idEsp32 = models.ForeignKey(Esp32Control, on_delete=models.CASCADE)


# Tablas auxiliares -----------------------------------------------------

class UltimaEsp32(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=10)
    fecha = models.DateTimeField()
    humedad_suelo = models.FloatField()
    idEsp32 = models.IntegerField()

class UltimaLecturaRaspberry(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField()
    humedad_ambiente = models.FloatField()
    temperatura_ambiente = models.FloatField()
    radiacion_solar = models.FloatField()
    presion_atmosferica = models.FloatField()
    velocidad_viento = models.FloatField()
    et0 = models.FloatField()
    ruta = models.CharField(max_length=100, default='')
    idRaspberry = models.IntegerField()

class DiarioLecturaRaspberry(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField()
    humedad_ambiente = models.FloatField()
    temperatura_ambiente = models.FloatField()
    radiacion_solar = models.FloatField()
    presion_atmosferica = models.FloatField()
    velocidad_viento = models.FloatField()
    et0 = models.FloatField()
    ruta = models.CharField(max_length=100, default='')
    idRaspberry = models.IntegerField()

class SemanaLecturaRaspberry(models.Model):
    id = models.AutoField(primary_key=True)
    semana = models.IntegerField()
    humedad_ambiente = models.FloatField()
    temperatura_ambiente = models.FloatField()
    radiacion_solar = models.FloatField()
    presion_atmosferica = models.FloatField()
    velocidad_viento = models.FloatField()
    et0 = models.FloatField()
    idRaspberry = models.IntegerField()

class MesLecturaRaspberry(models.Model):
    id = models.AutoField(primary_key=True)
    mes = models.IntegerField(default=0)
    humedad_ambiente = models.FloatField()
    temperatura_ambiente = models.FloatField()
    radiacion_solar = models.FloatField()
    presion_atmosferica = models.FloatField()
    velocidad_viento = models.FloatField()
    et0 = models.FloatField()
    idRaspberry = models.IntegerField()

class DiarioLecturaEsp32(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField()
    humedad_suelo = models.FloatField()
    idEsp32 = models.IntegerField()

class MesLecturaEsp32(models.Model):
    id = models.AutoField(primary_key=True)
    mes = models.IntegerField(default=0)
    humedad_suelo = models.FloatField()
    idEsp32 = models.IntegerField()







