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
    
class RaspberryDetail(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        raspberry = models.Raspberry.objects.get(id=pk)
        serializer = serializers.RaspberrySerializer(raspberry)
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
            # Guardar las lecturas en LecturaRaspberry
            serializer.save()
            # Actualizar la tabla UltimaLecturaRaspberry
            self.update_ultima_lectura(serializer.data)
            self.update_ultimas_siete_lecturas(serializer.data)


            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update_ultima_lectura(self, lecturas):
        # Manejo tanto de una lista de lecturas como de una única lectura
        if not isinstance(lecturas, list):
            listaLecturas = [lecturas]

        for lectura_data in listaLecturas:
            raspberry_id = lectura_data['idRaspberry']
            defaults = {
                'fecha': lectura_data['fecha'],
                'humedad_ambiente': lectura_data['humedad_ambiente'],
                'temperatura_ambiente': lectura_data['temperatura_ambiente'],
                'radiacion_solar': lectura_data['radiacion_solar'],
                'presion_atmosferica': lectura_data['presion_atmosferica'],
                'velocidad_viento': lectura_data['velocidad_viento'],
                'et0': lectura_data['et0'],
                'ruta': lectura_data['ruta'],
                'idRaspberry': raspberry_id
            }
            ultima_lectura, created = models.UltimaLecturaRaspberry.objects.update_or_create(
                idRaspberry=raspberry_id,
                defaults=defaults
            )

            # Usar el serializer para validar los datos antes de guardar
            ultima_lectura_serializer = serializers.UltimaLecturaRaspberrySerializer(ultima_lectura, data=defaults)
            if ultima_lectura_serializer.is_valid():
                ultima_lectura_serializer.save()
            else:
                raise ValueError(f"Error updating UltimaLecturaRaspberry: {ultima_lectura_serializer.errors}")
            
    def update_ultimas_siete_lecturas(self, lecturas):
        # Manejo tanto de una lista de lecturas como de una única lectura
        if not isinstance(lecturas, list):
            listaLecturas = [lecturas]

        for lectura_data in listaLecturas:
            raspberry_id = lectura_data['idRaspberry']
            fecha= lectura_data['fecha']
            fecha_mod =  datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%SZ')
            dia =fecha_mod.weekday()

            defaults = {
                'fecha': lectura_data['fecha'],
                'dia': dia,
                'humedad_ambiente': lectura_data['humedad_ambiente'],
                'temperatura_ambiente': lectura_data['temperatura_ambiente'],
                'radiacion_solar': lectura_data['radiacion_solar'],
                'presion_atmosferica': lectura_data['presion_atmosferica'],
                'velocidad_viento': lectura_data['velocidad_viento'],
                'et0': lectura_data['et0'],
                'ruta': lectura_data['ruta'],
                'idRaspberry': raspberry_id,
            }

            # Buscar si ya existe una entrada para este esp32_id y día de la semana
            try:
                ultima_lectura = models.SieteDiasAnterioresLecturaRaspberry.objects.get(
                    idRaspberry=raspberry_id,
                    dia=dia
                )
                # Actualizar el registro existente
                for attr, value in defaults.items():
                    setattr(ultima_lectura, attr, value)
                ultima_lectura.save()
                print("Actualizado el registro existente")

            except models.SieteDiasAnterioresLecturaRaspberry.DoesNotExist:
                # Crear un nuevo registro si no existe
                ultima_lectura = models.SieteDiasAnterioresLecturaRaspberry(**defaults)
                ultima_lectura.save()
                print("Creado un nuevo registro")
        
            # Usar el serializer para validar los datos antes de guardar
            ultima_lectura_serializer = serializers.SieteDiasAnterioresLecturaRaspberrySerializer(ultima_lectura, data=defaults)
            if ultima_lectura_serializer.is_valid():
                ultima_lectura_serializer.save()
            else:
                raise ValueError(f"Error updating UltimaRaspberry: {ultima_lectura_serializer.errors}")


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
            # Guardar las lecturas en LecturaEsp32
            serializer.save()
            # Actualizar la tabla UltimaEsp32
            self.update_ultima_lectura(serializer.data)
            # Actualizar la tabla SieteDiasAnterioresLecturaEsp32
            self.update_ultimas_siete_lecturas(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update_ultima_lectura(self, lecturas):
        # Manejo tanto de una lista de lecturas como de una única lectura
        if not isinstance(lecturas, list):
            listaLecturas = [lecturas]

        for lectura_data in listaLecturas:
            esp32_id = lectura_data['idEsp32']
            defaults = {
                'fecha': lectura_data['fecha'],
                'humedad_suelo': lectura_data['humedad_suelo'],
                'idEsp32': esp32_id
            }
            ultima_lectura, created = models.UltimaEsp32.objects.update_or_create(
                idEsp32=esp32_id,
                defaults=defaults
            )

            # Usar el serializer para validar los datos antes de guardar
            ultima_lectura_serializer = serializers.UltimaEsp32Serializer(ultima_lectura, data=defaults)
            if ultima_lectura_serializer.is_valid():
                ultima_lectura_serializer.save()
            else:
                raise ValueError(f"Error updating UltimaEsp32: {ultima_lectura_serializer.errors}")
            
    def update_ultimas_siete_lecturas(self, lecturas):
        # Manejo tanto de una lista de lecturas como de una única lectura
        if not isinstance(lecturas, list):
            listaLecturas = [lecturas]

        for lectura_data in listaLecturas:
            esp32_id = lectura_data['idEsp32']
            fecha= lectura_data['fecha']
            fecha_mod =  datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%SZ')
            dia =fecha_mod.weekday()

            defaults = {
                'fecha': lectura_data['fecha'],
                'humedad_suelo': lectura_data['humedad_suelo'],
                'idEsp32': esp32_id,
                'dia': dia
            }
            # Buscar si ya existe una entrada para este esp32_id y día de la semana
            try:
                ultima_lectura = models.SieteDiasAnterioresLecturaEsp32.objects.get(
                    idEsp32=esp32_id,
                    dia=dia
                )
                # Actualizar el registro existente
                for attr, value in defaults.items():
                    setattr(ultima_lectura, attr, value)
                ultima_lectura.save()
                print("Actualizado el registro existente")

            except models.SieteDiasAnterioresLecturaEsp32.DoesNotExist:
                # Crear un nuevo registro si no existe
                ultima_lectura = models.SieteDiasAnterioresLecturaEsp32(**defaults)
                ultima_lectura.save()
                print("Creado un nuevo registro")
        
            # Usar el serializer para validar los datos antes de guardar
            ultima_lectura_serializer = serializers.SieteDiasAnterioresLecturaEsp32Serializer(ultima_lectura, data=defaults)
            if ultima_lectura_serializer.is_valid():
                ultima_lectura_serializer.save()
            else:
                raise ValueError(f"Error updating UltimaEsp32: {ultima_lectura_serializer.errors}")



    
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
    
    def put(self, request):
        programa = models.Programa.objects.get(id=request.data['id'])
        serializer = serializers.ProgramaSerializer(programa, data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        programa = models.Programa.objects.get(id=request.data['id'])
        programa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    

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
        

class Ultima_lectura_esp32(APIView):
    permission_classes = [AllowAny]
    def get(self, request, valvula):
        lectura = models.UltimaEsp32.objects.get(idEsp32=valvula)
        serializer = serializers.UltimaEsp32Serializer(lectura)
        return Response(serializer.data)

class Ultima_lectura_raspberry(APIView):
    permission_classes = [AllowAny]
    def get(self, request, raspberry):
        lectura = models.UltimaLecturaRaspberry.objects.get(idRaspberry=raspberry)
        serializer = serializers.UltimaLecturaRaspberrySerializer(lectura)
        return Response(serializer.data)
    

class Esp32_Usuario(APIView):
    permission_classes = [AllowAny]
    def get(self, request, usuario_id):
        try:
            usuario = models.Usuario.objects.get(id=usuario_id)
            raspberries = usuario.idRaspberry.all() 
            esp32s = models.Esp32Control.objects.filter(idRaspberry__in=raspberries)
            serializer = serializers.Esp32ControlSerializer(esp32s, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
class UltimaSemanaRaspberry(APIView):
    permission_classes = [AllowAny]
    def get(self, request, raspberry):
        lecturas = models.SemanaLecturaRaspberry.objects.filter(idRaspberry=raspberry)
        semana = datetime.now().isocalendar()[1]
        semana_anterior = semana - 1
        lecturas_semana = lecturas.filter(semana=semana_anterior)
        serializer = serializers.SemanaLecturaRaspberrySerializer(lecturas_semana, many=True)
        return Response(serializer.data)
    
class UltimaSemanaEsp32(APIView):
    permission_classes = [AllowAny]
    def get(self, request, esp32):
        lecturas = models.SemanaLecturaEsp32.objects.filter(idEsp32=esp32)
        semana = datetime.now().isocalendar()[1]
        semana_anterior = semana - 1
        lecturas_semana = lecturas.filter(semana=semana_anterior)
        serializer = serializers.SemanaLecturaEsp32Serializer(lecturas_semana, many=True)
        return Response(serializer.data)
    

class UltimosSieteDiasEsp32(APIView):
    permission_classes = [AllowAny]
    def get(self, request, esp32):
        lecturas = models.SieteDiasAnterioresLecturaEsp32.objects.filter(idEsp32=esp32)
        serializer = serializers.SieteDiasAnterioresLecturaEsp32Serializer(lecturas, many=True)
        return Response(serializer.data)

class UltimosSieteDiasRaspberry(APIView):
    permission_classes = [AllowAny]
    def get(self, request, raspberry):
        lecturas = models.SieteDiasAnterioresLecturaRaspberry.objects.filter(idRaspberry=raspberry)
        serializer = serializers.SieteDiasAnterioresLecturaRaspberrySerializer(lecturas, many=True)
        return Response(serializer.data)

class MensualRaspberry(APIView):
    permission_classes = [AllowAny]
    def get(self, request, raspberry):
        lecturas = models.MesLecturaRaspberry.objects.filter(idRaspberry=raspberry)
        serializer = serializers.MesLecturaRaspberrySerializer(lecturas, many=True)
        return Response(serializer.data)
    
class MensualEsp32(APIView):
    permission_classes = [AllowAny]
    def get(self, request, esp32):
        lecturas = models.MesLecturaEsp32.objects.filter(idEsp32=esp32)
        serializer = serializers.MesLecturaEsp32Serializer(lecturas, many=True)
        return Response(serializer.data)
    
class LecturasRaspberryPersonalizadas(APIView): 
    permission_classes = [AllowAny]
    def get(self, request, raspberry, fecha_inicio, fecha_fin):
        print(fecha_inicio)
        print(fecha_fin)
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
        except ValueError:
            return Response({'error': 'Formato de fecha inválido'}, status=400)

        lecturas = models.DiarioLecturaRaspberry.objects.filter(
            idRaspberry=raspberry,
            fecha__range=(fecha_inicio_dt, fecha_fin_dt)
        )
        serializer = serializers.DiarioLecturaRaspberrySerializer(lecturas, many=True)
        return Response(serializer.data)
    
class LecturasEsp32Personalizadas(APIView):
    permission_classes = [AllowAny]
    def get(self, request, esp32, fecha_inicio, fecha_fin):
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
        except ValueError:
            return Response({'error': 'Formato de fecha inválido'}, status=400)

        lecturas = models.DiarioLecturaEsp32.objects.filter(
            idEsp32=esp32,
            fecha__range=(fecha_inicio_dt, fecha_fin_dt)
        )
        serializer = serializers.DiarioLecturaEsp32Serializer(lecturas, many=True)
        return Response(serializer.data)


class UltimasImagenes(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk, num):
        try:
            lecturas = models.LecturaRaspberry.objects.filter(idRaspberry=pk).order_by('-id')[:num]
            serializer = serializers.LecturaRaspberrySerializer(lecturas, many=True)
            return Response(serializer.data)
        except models.LecturaRaspberry.DoesNotExist:
            return Response({'error': 'No hay imagenes registradas para este raspberry'}, status=404)

    
class UltimoRiegoProgramado(APIView):
    permission_classes = [AllowAny]
    def get(self, request, esp32):
        try:
            programa = models.Programa.objects.filter(idEsp32=esp32).latest('id')
            serializer = serializers.ProgramaSerializer(programa)
            return Response(serializer.data)
        except models.Programa.DoesNotExist:
            return Response({'error': 'No hay programas registrados para este esp32'}, status=404)
        
class DescargaEsp32(APIView):
    permission_classes = [AllowAny]
    def get(self, request, esp32):
        try:
            esp32 = models.Esp32Control.objects.get(id=esp32)
            serializer = serializers.Esp32ControlSerializer(esp32)
            return Response(serializer.data)
        except models.Esp32Control.DoesNotExist:
            return Response({'error': 'Esp32 no encontrado'}, status=404)
        
