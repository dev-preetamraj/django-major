import os
import magic
from django.conf import settings
from cloudinary import uploader, CloudinaryImage
from ..common.constants import HOST_NAME, ENTRY_STATIC_FOLDER

def get_mime_type(file):
    initial_pos = file.tell()
    file.seek(0)
    mime_type = magic.from_buffer(file.read(2048), mime=True)
    file.seek(initial_pos)
    return mime_type

def get_file_ext(mime_type):
    ext = mime_type.split('/')[-1]
    ext = f'.{ext}'
    return ext

def save_profile_return_url(profile_picture, username):
    directory = f'static/profile/'
    base_dir = settings.BASE_DIR
    path = os.path.join(base_dir, directory)
    if not os.path.exists(path):
        os.makedirs(path)
    file_content = profile_picture.read()
    mime_type = get_mime_type(profile_picture)
    file_ext = get_file_ext(mime_type)
    file_name = f'{username}{file_ext}'
    full_file_name = f'{directory}{file_name}'.replace(' ', '')
    with open(full_file_name, 'wb') as fi:
        fi.write(file_content)
        fi.close()
    profile_picture_url = f'{HOST_NAME}/static/profile/{file_name}'
    return profile_picture_url

def upload_profile_to_cloudinary(profile_picture, username):
    folder = f'{ENTRY_STATIC_FOLDER}/profile/'
    public_id = f'{username}_profile'
    file_ext = profile_picture.name.split('.')[-1]
    profile_picture.name = f'{username}_profile.{file_ext}'
    result = uploader.upload(
        profile_picture,
        folder=folder,
        public_id=public_id,
        overwrite = True,
        invalidate = True
    )
    # img_url = CloudinaryImage(f'{folder}{profile_picture.name}').build_url(
    #     width=300,
    #     height=300,
    #     gravity='faces',
    #     crop='fill'
    # )
    return result.get('secure_url')