from django.urls import path
from . import views
from .views import CustomLoginView


urlpatterns = [
    path('',views.index,name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('registro/', views.register, name='registro'),
    path('verificacion/<str:username>/', views.verify, name="verificacion")

]
