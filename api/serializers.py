from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from . import models

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rol
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    idRaspberry = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = models.Usuario
        fields = '__all__'
    
    def create(self, validated_data):
        raspberries = validated_data.pop('idRaspberry', [])
        password = validated_data.pop('password')
        usuario = models.Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()

        # Asocia las Raspberries con el usuario
        usuario.idRaspberry.set(raspberries)

        return usuario
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    @classmethod
    def get_username_field(cls):
        return 'username'  # Campo utilizado para identificar al usuario

class RaspberrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Raspberry
        fields = '__all__'

class Esp32HumedadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Esp32Humedad
        fields = '__all__'

class Esp32ControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Esp32Control
        fields = '__all__'
        
class LecturaRaspberrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LecturaRaspberry
        fields = '__all__'

class LecturaEsp32Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.LecturaEsp32
        fields = '__all__'

class ProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Programa
        fields = '__all__'

class UltimaEsp32Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.UltimaEsp32
        fields = '__all__'

class UltimaLecturaRaspberrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UltimaLecturaRaspberry
        fields = '__all__'

class DiarioLecturaRaspberrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DiarioLecturaRaspberry
        fields = '__all__'

class SemanaLecturaRaspberrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SemanaLecturaRaspberry
        fields = '__all__'

class MesLecturaRaspberrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MesLecturaRaspberry
        fields = '__all__'   

class DiarioLecturaEsp32Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.DiarioLecturaEsp32
        fields = '__all__'

class MesLecturaEsp32Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.MesLecturaEsp32
        fields = '__all__'
