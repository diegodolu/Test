from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from . import models
from . import serializers

from .permissions import IsDeveloper
from django.core.mail import send_mail
from rest_framework.response import Response
from django.conf import settings
from datetime import datetime, timedelta
from django.db.models import Avg

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer
    
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsDeveloper])
def register_user(request):
    print(f'User: {request.user.idRol.categoria}')  # Imprime el usuario autenticado
    print(f'Request Data: {request.data}')  # Imprime el cuerpo de la solicitud

    serializer = serializers.UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RolList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        roles = models.Rol.objects.all()
        serializer = serializers.RolSerializer(roles, many=True)
        return Response(serializer.data)

class UsuarioList(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    def get(self, request):
        usuarios = models.Usuario.objects.all()
        serializer = serializers.UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)
    
class UsuarioDetail(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        usuario = models.Usuario.objects.get(id=pk)
        serializer = serializers.UsuarioSerializer(usuario)
        return Response(serializer.data)

class RaspberryList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        raspberries = models.Raspberry.objects.all()
        serializer = serializers.RaspberrySerializer(raspberries, many=True)
        return Response(serializer.data)

class Esp32HumedadList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        esp32s = models.Esp32Humedad.objects.all()
        serializer = serializers.Esp32Serializer(esp32s, many=True)
        return Response(serializer.data)

class LecturaRaspberryList(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        lecturas = models.LecturaRaspberry.objects.all()
        serializer = serializers.LecturaRaspberrySerializer(lecturas, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if isinstance(request.data, list):
            # Si se recibe una lista de lecturas, se realiza una inserción masiva
            serializer = serializers.LecturaRaspberrySerializer(data=request.data, many=True)
        else:
            # Si se recibe un solo objeto, se realiza una inserción individual
            serializer = serializers.LecturaRaspberrySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LecturaEsp32List(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        lecturas = models.LecturaEsp32.objects.all()
        serializer = serializers.LecturaEsp32Serializer(lecturas, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if isinstance(request.data, list):
            # Si se recibe una lista de lecturas, se realiza una inserción masiva
            serializer = serializers.LecturaEsp32Serializer(data=request.data, many=True)
        else:
            # Si se recibe un solo objeto, se realiza una inserción individual
            serializer = serializers.LecturaEsp32Serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProgramaList(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        programas = models.Programa.objects.all()
        serializer = serializers.ProgramaSerializer(programas, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if isinstance(request.data, list):
            # Si se recibe una lista de programas, se realiza una inserción masiva
            serializer = serializers.ProgramaSerializer(data=request.data, many=True)
        else:
            # Si se recibe un solo objeto, se realiza una inserción individual
            serializer = serializers.ProgramaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProgramaWeek(APIView):
    permission_classes = [AllowAny]
    def get(self, request, semana):
        programas = models.Programa.objects.filter(semana=semana)
        serializer = serializers.ProgramaSerializer(programas, many=True)
        return Response(serializer.data)
    
class RequestPasswordReset(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        user = models.Usuario.objects.filter(email=email).first()
        if user:
            token = models.PasswordResetToken.objects.create(user=user)
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{token.token}"
            send_mail(
                'Recuperación de contraseña',
                f'Usa este enlace para restablecer tu contraseña: {reset_url}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        return Response({"message": "Si tu correo electrónico está registrado, recibirás un enlace para restablecer tu contraseña."})



class ResetPassword(APIView):
    permission_classes = [AllowAny] 
    def post(self, request, token):
        new_password = request.data.get('password')
        try:
            reset_token = models.PasswordResetToken.objects.get(token=token)
            user = reset_token.user
            user.password = make_password(new_password)
            user.save()
            reset_token.delete()  # Eliminar el token después de su uso
            return Response({"message": "Contraseña restablecida correctamente."})
        except models.PasswordResetToken.DoesNotExist:
            return Response({"error": "Token inválido."}, status=400)
        

