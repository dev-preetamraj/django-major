import logging
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView


from .queries import (
    get_user_by_email,
    get_user_by_username,
    register_user,
    get_actual_user_by_username
)

from core.utils.password_utils import verify_password
from .utils import generate_access_token, generate_refresh_token, regenerate_token

logger = logging.getLogger('accounts')

class RegisterUser(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        try:
            data = request.data
            if not 'name' in data:
                data['name'] = None
            if not 'profile_picture' in data:
                data['profile_picture'] = None

            if not 'username' in data:
                return Response({
                    'error': 'username is required field',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            username = data['username']

            if not 'email' in data:
                return Response({
                    'error': 'email is required field',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            email = data['email']

            if not 'password' in data:
                return Response({
                    'error': 'password is required field',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            password = data['password']

            if not 'password1' in data:
                return Response({
                    'error': 'password1 is required field',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            password1 = data['password1']
            
            if get_user_by_email(email):
                return Response({
                    'error': 'User with this email already exists',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)

            if get_user_by_username(username):
                return Response({
                    'error': 'User with this username already exists',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)

            if len(password) < 8:
                return Response({
                    'error': 'Password must be 8 or more characters long',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)

            if password != password1:
                return Response({
                    'error': 'Password did not matched',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)

            user = register_user(data)
            return Response({
                'success': 'User created successfully',
                'data': user
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f'views/RegisterUser/post: {e}')
            return Response({
                'error': 'Something went wrong. We are working on it!',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Authorization(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, slug):
        try:
            if slug == 'authorize':
                data = request.data
                if 'username' not in data:
                    return Response({
                        'error': 'username is required field',
                        'data': None
                    }, status=status.HTTP_400_BAD_REQUEST)
                if 'password' not in data:
                    return Response({
                        'error': 'password is required field',
                        'data': None
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                user = get_actual_user_by_username(data['username'])
                if user is None:
                    return Response({
                        'error': 'User not found',
                        'data': None
                    }, status=status.HTTP_404_NOT_FOUND)
                    
                if not verify_password(data['password'], user['password']):
                    return Response({
                        'error': 'Incorrect password',
                        'data': None
                    }, status=status.HTTP_401_UNAUTHORIZED)
                
                access_token = generate_access_token(user['user_id'])
                refresh_token = generate_refresh_token(user['user_id'])

                return Response({
                    'success': 'Authentication successful',
                    'data': {
                        'access_token': access_token,
                        'refresh_token': refresh_token
                    }
                }, status=status.HTTP_200_OK)

            elif slug == 'regenerate-token':
                data = request.data
                if 'refresh_token' not in data:
                    return Response({
                        'error': 'refresh_token is required field',
                        'data': None
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                return regenerate_token(data['refresh_token'])

        except Exception as e:
            logger.error(f'views/Authorization/post: {e}')
            return Response({
                'error': 'Something went wrong. We are working on it!',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)