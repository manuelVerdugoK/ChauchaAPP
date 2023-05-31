from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'aplicacion'

urlpatterns = [
    path('Index',login_required(views.index),name='index'),
    
]
