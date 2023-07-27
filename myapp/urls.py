from django.contrib import admin
from django.urls import path, include

urlpatterns = [
<<<<<<< HEAD
    path('admin/', admin.site.urls), #Specifies path to admin webpage
    path('', include('mainapp.urls')), #Specifies path to login webpage
=======
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls')),
>>>>>>> 9b9425f00591eb859dc79da1809734c02945206a
]
