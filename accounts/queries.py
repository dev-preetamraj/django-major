import logging

from django.conf import settings
from sqlalchemy.orm import Session
from .models import User
from core.utils.password_utils import hash_password
from core.utils.data_formatters import row2dict
from core.utils.file_utils import save_profile_return_url, upload_profile_to_cloudinary

logger = logging.getLogger('accounts')
session: Session = settings.DB_SESSION

def get_user_by_email(email):
    is_user = False
    try:
        user = session.query(User).filter(User.email==email).first()
        session.commit()
        if user:
            is_user = True
    except Exception as e:
        logger.error(f'queries/get_user_by_email: {e}')
        session.rollback()
        is_user = False
    return is_user

def get_user_by_username(username):
    is_user = False
    try:
        user = session.query(User).filter(User.username==username).first()
        session.commit()
        if user:
            is_user = True
    except Exception as e:
        logger.error(f'queries/get_user_by_username: {e}')
        session.rollback()
        is_user = False

    return is_user

def register_user(data):
    user = None
    try:
        name = data['name']
        username = data['username']
        email = data['email']
        password = data['password']
        profile_picture = data['profile_picture']

        profile_picture_url = None
        if profile_picture is not None:
            # profile_picture_url = save_profile_return_url(profile_picture, username)
            profile_picture_url = upload_profile_to_cloudinary(profile_picture, username)

        hashed_password = hash_password(password)
        new_user = User(
            name = name,
            username = username,
            email = email,
            password = hashed_password,
            profile_picture = profile_picture_url
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        user = new_user

    except Exception as e:
        logger.error(f'queries/register_user: {e}')
        session.rollback()
        user = None

    return row2dict(user)

def get_user(user_id):
    try:
        user = session.query(
            User.user_id.label('user_id')
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

def get_actual_user_by_username(username):
    try:
        user = session.query(User).filter(User.username==username).one_or_none()
        if user:
            return row2dict(user)
        return None
    except Exception as e:
        logger.error(f'queries/get_actual_user_by_username: {e}')
        session.rollback()
        return None