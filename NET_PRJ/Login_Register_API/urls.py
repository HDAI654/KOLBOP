from django.urls import path, include
from .views import *

urlpatterns = [
    path('reg/<str:us>/<str:psw>/<str:tkn>', reg, name='register'),
    path('login/<str:us>/<str:psw>', login, name='login'),
    path('del_acc/<str:us>/<str:psw>', del_acc, name='delete account'),
]