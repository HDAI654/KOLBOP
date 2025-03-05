from django.urls import path, include
from .views import *

urlpatterns = [
    path('', MyModelList.as_view(), name='model list'),
    path('get_files/<str:tkn>/<str:user>', return_uploaded_files, name='return uploaded files'),
    path('get_names/<str:tkn>/<str:user>', return_uploaded_files_names, name='return uploaded files names'),
    path('delete_all_files/<str:tkn>/<str:user>', delete_all_files, name='delete all files'),
    path('delete_one_file', delete_one_file, name='delete one file'),
    path('panel', show_saved, name='show_saved'),
    path('login', login_page, name='login'),
    path('check_login', check_login, name='check login'),
    path('logout', logout_func, name='logout'),
]