from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('APAS/', admin.site.urls),
    path('bkup/', include("BackUpAPI.urls")),
    path('auth/', include("Login_Register_API.urls")),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)