# Django | DRF

This project uses `Django` and `Django Rest Framework` with standard industrial practices which will work for production too. This project will show you some best practices that we should keep in mind while developing `APIs` with `DRF`.

## Technologies Used:
1. Django
1. Django Rest Framework
1. SqlAlchemy: Python SQL toolkit and ORM
1. Alembic: Database migration tool
1. MySQL: Database
1. Cloudinary: For serving static files

## Use the project in your PC
- Clone the project
    ```bash
    ~ git clone git@github.com:iitianpreetam/django-major.git
    ```
- Change directory
    ```bash
    ~ cd django-major
    ```
- Create a Virtual Environment
    ```bash
    ~ python -m venv env
    ```
- Activate the Virtual Environment
    ```bash
    Windows
    ~ .\env\Scripts\activate

    Linux or MacOS
    ~ source env/bin/activate
    ```
- Install requirements
    ```bash
    ~ pip install -r requirements.txt
    ```
- create a `.env` file and update the following details
    ```py
    DB_HOST=<YOUR_DB_HOST>
    DB_NAME=<YOUR_DB_NAME>
    DB_USER=<YOUR_DB_USER>
    DB_PASSWORD=<YOUR_DB_PASSWORD>
    DB_PORT=<YOUR_DB_PORT>
    CLOUD_NAME=<YOUR_CLOUDINARY_CLOUD_NAME>
    API_KEY=<YOUR_CLOUDINARY_API_KEY>
    API_SECRET=<YOUR_CLOUDINARY_API_SECRET>
    SECRET_KEY=<YOUR_DJANGO_SECRET_KEY>
    REFRESH_SECRET_KEY=<YOUR_REFRESH_SECRET_KEY>
    ```
- Migrate tables
    ```bash
    ~ alembic revision --autogenerate -m "initial migration"
    ~ alembic upgrade head
    ```

- Run Development Server
    ```bash
    ~ python manage.py runserver
    OR
    ~ python3 manage.py runserver
    ```

    `Note:` Do not mess up folder structure as it will conflic with imports.
