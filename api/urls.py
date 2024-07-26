from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # urls generales
    path('roles/', views.RolList.as_view()),
    path('usuarios/', views.UsuarioList.as_view()),
    path('usuarios/<int:pk>/', views.UsuarioDetail.as_view()),
    path('raspberries/', views.RaspberryList.as_view()),
    path('esp32/', views.Esp32HumedadList.as_view()),
    path('lecturasRaspberry/', views.LecturaRaspberryList.as_view()),
    path('lecturasEsp32/', views.LecturaEsp32List.as_view()),
    path('programas/', views.ProgramaList.as_view()),
    path('programaWeek/<int:semana>/', views.ProgramaWeek.as_view()),

    # urls para Dashboard - Monitoreo
    path('lecturasEsp32/ultima/<int:valvula>/', views.Ultima_lectura_esp32.as_view()),
    path('lecturasRaspberry/ultima/<int:raspberry>/', views.Ultima_lectura_raspberry.as_view()),
    path('esp32/<int:usuario_id>/', views.Esp32_Usuario.as_view()), # también se usa en Dashboard - Sensores

    # urls para Dashboard - Historial ----> Estación meteológica
    path('lecturasRaspberry/ultimaSemana/<int:raspberry>/', views.UltimaSemanaRaspberry.as_view()), #funcional pero no se usa por el momento
    path('lecturasRaspberry/ultimosSieteDiasEsp32/<int:esp32>/', views.UltimosSieteDiasEsp32.as_view()), 
    path('lecturasRaspberry/ultimosSieteDiasRaspberry/<int:raspberry>/', views.UltimosSieteDiasRaspberry.as_view()), 
    path('lecturasRaspberry/mensual/<int:raspberry>/', views.MensualRaspberry.as_view()),
    path('lecturasEsp32/mensual/<int:esp32>/', views.MensualEsp32.as_view()),
    path('lecturasRaspberry/<int:raspberry>/<str:fecha_inicio>/<str:fecha_fin>/', views.LecturasRaspberryPersonalizadas.as_view()), # la fecha debe tener un formato 'YYYY-MM-DD'
    path('lecturasEsp32/<int:esp32>/<str:fecha_inicio>/<str:fecha_fin>/', views.LecturasEsp32Personalizadas.as_view()), # la fecha debe tener un formato 'YYYY-MM-DD'

    #urls para Dashboard - Sensores
    path('raspberries/<int:pk>/', views.RaspberryDetail.as_view()),

    #urls para Dashboard - Campo
    path('lecturasRaspberry/<int:pk>/ultimasImagenes/<int:num>', views.UltimasImagenes.as_view()),

    # urls para obtener token de acceso y token de actualización
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    # urls para registrar usuario
    path('register/', views.register_user, name='register_user'),

    path('request-password-reset/', views.RequestPasswordReset.as_view(), name='request-password-reset'),
    path('reset-password/<uuid:token>/', views.ResetPassword.as_view(), name='reset-password'),
]