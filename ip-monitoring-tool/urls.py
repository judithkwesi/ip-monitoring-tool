from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('cp1/', admin.site.urls), #Specifies path to admin webpage
    path('', include('mainapp.urls')), #Specifies path to login webpage
]
