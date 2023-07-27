from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), #Specifies path to admin webpage
    path('', include('mainapp.urls')), #Specifies path to login webpage
]
