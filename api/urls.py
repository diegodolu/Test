from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('roles/', views.RolList.as_view()),
    path('usuarios/', views.UsuarioList.as_view()),
    path('usuarios/<int:pk>/', views.UsuarioDetail.as_view()),
    path('raspberries/', views.RaspberryList.as_view()),
    path('esp32/', views.Esp32HumedadList.as_view()),
    path('lecturasRaspberry/', views.LecturaRaspberryList.as_view()),
    path('lecturasEsp32/', views.LecturaEsp32List.as_view()),
    path('programas/', views.ProgramaList.as_view()),
    path('programaWeek/<int:semana>/', views.ProgramaWeek.as_view()),


    # urls para obtener token de acceso y token de actualización
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    # urls para registrar usuario
    path('register/', views.register_user, name='register_user'),

    path('request-password-reset/', views.RequestPasswordReset.as_view(), name='request-password-reset'),
    path('reset-password/<uuid:token>/', views.ResetPassword.as_view(), name='reset-password'),
]