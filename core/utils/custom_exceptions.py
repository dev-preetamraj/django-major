from rest_framework import status
from rest_framework.exceptions import APIException

class ExpiredSignatureError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Access Token has Expired'
    default_code = 'expired_signature_error'

class InvalidSignatureError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Invalid Token'
    default_code = 'invalid_signature_error'

class DecodeError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Header String Manipulated'
    default_code = 'decode_error'

class InvalidTokenError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Invalid Token'
    default_code = 'invalid_token_error'