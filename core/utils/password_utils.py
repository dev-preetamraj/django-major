from django.contrib.auth.hashers import make_password, check_password

def hash_password(password):
    return make_password(password)

def verify_password(plain_pwd, hashed_pwd):
    return check_password(plain_pwd, hashed_pwd)