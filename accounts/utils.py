from datetime import datetime, timedelta
import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from .queries import get_user

def generate_access_token(user_id):
    access_token_payload = {
        'user_id': user_id,
        'exp': (
            datetime.utcnow() + 
            timedelta(
                days=0, minutes=settings.ACCESS_TOKEN_EXPIRY
            )
        ),
        'iat': datetime.utcnow()
    }

    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')
    return access_token

def generate_refresh_token(user_id):
    refresh_token_payload = {
        'user_id': user_id,
        'exp': (
            datetime.utcnow() + 
            timedelta(
                days=0, minutes=settings.REFRESH_TOKEN_EXPIRY
            )
        ),
        'iat': datetime.utcnow()
    }
    refresh_token = jwt.encode(refresh_token_payload, settings.REFRESH_SECRET_KEY, algorithm='HS256')
    return refresh_token

def regenerate_token(refresh_token):
    try:
        payload = jwt.decode(refresh_token, settings.REFRESH_SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('user_id')
        user = get_user(user_id)

        if user:
            data = {
                'access_token': generate_access_token(user_id),
                'refresh_token': generate_refresh_token(user_id)
            }
            return Response({
                'success': 'Token Refreshed Successfully',
                'data': data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'error': 'User not Found',
            'data': None
        }, status=status.HTTP_404_NOT_FOUND)

    except jwt.ExpiredSignatureError:
        return Response({
            'error': 'Refresh Token has Expired',
            'data': None
        }, status=status.HTTP_403_FORBIDDEN)
    
    except jwt.InvalidSignatureError:
        return Response({
            'error': 'Invalid Token',
            'data': None
        }, status=status.HTTP_403_FORBIDDEN)

    except jwt.DecodeError:
        return Response({
            'error': 'Header String Manipulated',
            'data': None
        }, status=status.HTTP_403_FORBIDDEN)

    except jwt.InvalidTokenError:
        return Response({
            'error': 'Invalid Token',
            'data': None
        }, status=status.HTTP_403_FORBIDDEN)