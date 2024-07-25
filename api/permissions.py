from rest_framework.permissions import BasePermission

class IsDeveloper(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            # Verifica si el usuario tiene el rol con idRol igual a 3
            if request.user.idRol.categoria == 'Desarrollador':
                return True
        return False