import logging
import jwt
from django.conf import settings

from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .queries import get_user

from core.utils import custom_exceptions as ce

# Get an instance of logger
logger = logging.getLogger('accounts')

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            authorization_header = request.headers.get('Authorization')

            if authorization_header:
                access_token = authorization_header.split(' ')[1]

                payload = jwt.decode(
                    access_token,
                    settings.SECRET_KEY,
                    algorithms=['HS256']
                )

                user = get_user(user_id=payload.get('user_id'))
                if user:
                    return (user, None)
                else:
                    raise exceptions.NotFound(detail='User not found. Invalid credentials')
            
            raise exceptions.AuthenticationFailed

        except jwt.ExpiredSignatureError:
            raise ce.ExpiredSignatureError
        
        except jwt.InvalidSignatureError:
            raise ce.InvalidSignatureError

        except jwt.DecodeError:
            raise ce.DecodeError

        except jwt.InvalidTokenError:
            raise ce.InvalidTokenError