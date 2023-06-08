from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'aplicacion'

urlpatterns = [
    path('Index/',login_required(views.index),name='index'),
    path('log_out/', views.log_out, name='log_out'),
    path('MisEspacios/',login_required(views.ver_espacios),name="ver_espacios"),
    path('unirse-espacio/', views.unirse_espacio, name='unirse_espacio'),
    path('Mi-Hoja-financiera/',views.hoja_informacion_financiera,name="hoja_financiera"),
    path('Mi-Espacio/<int:espacio_id>/', views.mi_espacio, name='miEspacio'),

    path('eliminar/<int:espacio_id>/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('enviar_invitacion/<int:espacio_id>/', views.enviar_invitacion, name='enviar_invitacion'),


    path('eliminar_ingreso/<int:ingreso_id>/', views.eliminar_ingreso, name='eliminar_ingreso'),
    path('eliminar_egreso/<int:egreso_id>/', views.eliminar_egreso, name='eliminar_egreso'),
    path('AbandonarEspacio/<int:id_espacio>/',views.abandonar_espacio,name='abandonar_espacio'),
    path('DisolverEspacio/<int:id_espacio>/',views.disolver_espacio,name='disolver_espacio')
]
