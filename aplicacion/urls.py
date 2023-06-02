from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'aplicacion'

urlpatterns = [
    path('Index/',login_required(views.index),name='index'),
    path('log_out/', views.log_out, name='log_out'),
    path('MisEspacios/',login_required(views.ver_espacios),name="ver_espacios")
]
