from rest_framework.permissions  import BasePermission, SAFE_METHODS
from rest_framework.views import exception_handler

from django.utils import timezone


class CustomIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            from users.models import User
            User.objects.filter(id=request.user.id).update(is_online=timezone.now())
            return True
        else:
            return False

class CustomIsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method  in SAFE_METHODS:
            return True
            
        if request.user and request.user.is_authenticated:
            from users.models import User
            User.objects.filter(id=request.user.id).update(is_online=timezone.now())
            return True
        else:
            return False


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        return response

    exc_list = str(exc).split("DETAIL: ")

    return Response({"error": exc_list[-1]}, status=403)