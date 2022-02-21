from .main import *
from django.utils import timezone


expire = JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': user.username,
        'Expire on': timezone.now() + expire
    }
