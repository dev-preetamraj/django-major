import logging

from django.conf import settings
from sqlalchemy.orm import Session
from .models import User
from core.utils.password_utils import hash_password
from core.utils.data_formatters import row2dict
from core.utils.file_utils import save_profile_return_url, upload_profile_to_cloudinary

logger = logging.getLogger('accounts')
session: Session = settings.DB_SESSION

def is_user_by_email(email):
    try:
        user = session.query(User).filter(User.email==email).first()
        session.commit()
        if user:
            return True
        return False
    except Exception as e:
        logger.error(f'queries/is_user_by_email: {e}')
        session.rollback()
        return False

def is_user_by_username(username):
    try:
        user = session.query(User).filter(User.username==username).first()
        session.commit()
        if user:
            return True
        return False
    except Exception as e:
        logger.error(f'queries/is_user_by_username: {e}')
        session.rollback()
        return False

def register_user(data):
    try:
        username = data['username']
        email = data['email']
        first_name = data['first_name']
        last_name = data['first_name']
        password = data['password']
        profile_picture = data['profile_picture']
        dob = data['dob']
        age = data['age']
        gender = data['gender']
        address = data['address']
        is_hod = data['is_hod']
        is_staff = data['is_staff']
        is_teacher = data['is_teacher']
        is_student = data['is_student']

        profile_picture_url = None
        if profile_picture is not None:
            # profile_picture_url = save_profile_return_url(profile_picture, username)
            profile_picture_url = upload_profile_to_cloudinary(profile_picture, username)

        hashed_password = hash_password(password)
        new_user = User(
            username = username,
            email = email,
            first_name = first_name,
            last_name = last_name,
            password = hashed_password,
            profile_picture = profile_picture_url,
            dob = dob,
            age = age,
            gender = gender,
            address = address,
            is_hod = is_hod,
            is_staff = is_staff,
            is_teacher = is_teacher,
            is_student = is_student,
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        data = row2dict(new_user)
        data.pop('password')
        return data

    except Exception as e:
        logger.error(f'queries/register_user: {e}')
        session.rollback()
        return None

def get_user(user_id):
    try:
        user = session.query(
            User
        ).filter(
            User.user_id==user_id,
            User.is_active==1
        ).one_or_none()
        session.commit()
        if user:
            return row2dict(user)
        return None
    except Exception as e:
        logger.error(f'queries/get_user: {e}')
        session.rollback()
        return None

def get_user_by_username(username):
    try:
        user = session.query(User).filter(User.username==username).one_or_none()
        if user:
            return row2dict(user)
        return None
    except Exception as e:
        logger.error(f'queries/get_user_by_username: {e}')
        session.rollback()
        return None