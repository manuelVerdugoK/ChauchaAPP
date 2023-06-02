from django.contrib import admin
from django.urls import path, include
from myapp import urls as myapp_urls
from aplicacion import urls as aplicacion_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(myapp_urls)),
    path('App/', include(aplicacion_urls)),
]
