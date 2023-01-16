from django.urls import path
from .views import (
    RegisterUser,
    Authorization
)

urlpatterns = [
    path('register', RegisterUser.as_view(), name='register'),
    path('<str:slug>', Authorization.as_view(), name='authorization')
]