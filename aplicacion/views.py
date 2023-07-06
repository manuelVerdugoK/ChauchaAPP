from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import EspacioForm,IngresoForm,EgresoForm
from .models import Espacio,Ingreso,HojaInformacionFinanciera,Egreso
from django.shortcuts import get_object_or_404
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from myapp.models import UserProfile
from django.contrib.auth.models import User


from django.core.mail import send_mail
from django.conf import settings

from django.db.models import Sum
#import matplotlib.pyplot as plt 


# Create your views here.
@login_required
def index(request):
    if request.method == 'POST':
        form = EspacioForm(request.POST)
        if form.is_valid():
            espacio = form.save(commit=False)
            espacio.propietario_id = request.user.id  # Asignar el ID del usuario autenticado
            espacio.save()
            # Realiza cualquier redireccionamiento o respuesta necesaria después de guardar
            return redirect('aplicacion:ver_espacios')
    else:
        form = EspacioForm()
    return render(request, 'index.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect (reverse('myapp:index'))
    
@login_required
def ver_espacios(request):
    if request.method == 'POST':
        form = EspacioForm(request.POST)
        if form.is_valid():
            espacio = form.save(commit=False)
            espacio.propietario_id = request.user.id  # Asignar el ID del usuario autenticado
            espacio.save()
            # Realiza cualquier redireccionamiento o respuesta necesaria después de guardar
            return render(request,'index.html',{'form': form})
    else:
        form = EspacioForm()    
    espacios = Espacio.objects.filter(usuarios=request.user)

    return render(request, 'ver_espacios.html', {'espacios': espacios,'form': form})

#def mi_espacio(request):
#    espacio = Espacio.objects.get(usuarios=request.user)
#    usuarios = espacio.usuarios.all()
#    total_usuarios = usuarios.count()
#    usuarios = [usuario.username for usuario in espacio.usuarios.all()] 
#    return render (request,'espacio.html',{'espacio':espacio,'usuarios':usuarios,'total_usuarios':total_usuarios})



def unirse_espacio(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')  # Obtener el código ingresado en el formulario
        try:
            espacio = Espacio.objects.get(codigo_invitacion=codigo)  # Obtener el espacio con el código ingresado
        except Espacio.DoesNotExist:
            # El código no coincide con ningún espacio existente, mostrar mensaje de error
            return render(request, 'index.html.html', {'error': 'Código de invitación inválido.'})

        # El código es válido, agregar al usuario al espacio
        espacio.usuarios.add(request.user)

        # Determinar la URL de redirección en función de la vista desde la cual se llamó a unirse_espacio
        referer = request.META.get('HTTP_REFERER')
        if referer and 'MisEspacios' in referer:
            return redirect('aplicacion:ver_espacios')
        else:
            return redirect('aplicacion:index')

    return redirect('aplicacion:index')



def hoja_informacion_financiera(request):
    hoja = HojaInformacionFinanciera.objects.get(propietario=request.user)
    ingresos = hoja.ingreso_set.all()
    egresos = hoja.egreso_set.all()
    
    if request.method == 'POST':
        form1 = IngresoForm(request.POST)
        form2 = EgresoForm(request.POST)
        
        if form1.is_valid():
            ingreso = form1.save(commit=False)
            ingreso.hoja_informacion_financiera = hoja
            ingreso.save()
        
        if form2.is_valid():
            egreso = form2.save(commit=False)
            egreso.hoja_informacion_financiera = hoja
            egreso.save()
            
            return redirect('aplicacion:hoja_financiera')
        
    else:
        form1 = IngresoForm()
        form2 = EgresoForm()
    
    return render(request, 'hoja_financiera.html', {'ingresos': ingresos, 'egresos': egresos, 'form': form1, 'form2': form2})




def mi_espacio(request,espacio_id):
    if request.method == 'POST':
        form = EspacioForm(request.POST)
        if form.is_valid():
            espacio = form.save(commit=False)
            espacio.propietario_id = request.user.id  # Asignar el ID del usuario autenticado
            espacio.save()
            # Realiza cualquier redireccionamiento o respuesta necesaria después de guardar
            


            espacio = Espacio.objects.get(usuarios=request.user,id=espacio_id)
            creador = espacio.propietario.username
            usuarios = espacio.usuarios.all()
            print(type(creador))
            print(type(usuarios))

            colors = ['rgb(72, 199, 44)', 'rgb(220, 144, 31)', 'rgb(58, 104, 168)','rgb(147, 39, 210)']   # Ejemplo de lista de colores


            # Obtener todos los ingresos y egresos de los usuarios
            ingresos = Ingreso.objects.filter(hoja_informacion_financiera__propietario__in=usuarios)
            egresos = Egreso.objects.filter(hoja_informacion_financiera__propietario__in=usuarios)
            

            fuente_egreso_labels = []
            monto_egreso_values = []

            for egreso in egresos:
                fuente_egreso_labels.append(egreso.get_fuente_egreso_display())
                monto_egreso_values.append(float(egreso.monto_egreso))
            fig0 = go.Figure(data=[go.Bar(x=fuente_egreso_labels, y=monto_egreso_values,marker=dict(color=colors))])

            # Personaliza el diseño del gráfico
            fig0.update_layout(
                title="Montos asociados a fuente de egreso",
                xaxis_title="Fuente de egreso",
                yaxis_title="Monto de egreso",
            )

            # Convierte el gráfico en formato JSON
            graph_json = fig0.to_json()

            # Calcular el total de ingresos y egresos por tipo
            total_ingresos_tipo = ingresos.values('tipo_ingreso').annotate(total=Sum('monto_ingreso')).order_by('-total')
            total_egresos_tipo = egresos.values('tipo_egreso').annotate(total=Sum('monto_egreso')).order_by('-total')

            # Calcular el total de ingresos y egresos
            total_ingresos = ingresos.aggregate(total=Sum('monto_ingreso'))['total']
            total_egresos = egresos.aggregate(total=Sum('monto_egreso'))['total']

            # Crear una lista de tipos de ingreso y egreso
            tipos_ingreso = [ingreso['tipo_ingreso'] for ingreso in total_ingresos_tipo]
            tipos_egreso = [egreso['tipo_egreso'] for egreso in total_egresos_tipo]

            # Crear una lista de montos de ingreso y egreso
            montos_ingreso = [ingreso['total'] for ingreso in total_ingresos_tipo]
            montos_egreso = [egreso['total'] for egreso in total_egresos_tipo]

            # Calcular los porcentajes de ingresos y egresos
            porcentajes_ingreso = [(monto / total_ingresos) * 100 for monto in montos_ingreso]
            porcentajes_egreso = [(monto / total_egresos) * 100 for monto in montos_egreso]

            # Crear el gráfico de torta para los ingresos por tipo
            fig1 = go.Figure(data=[go.Pie(labels=tipos_ingreso, values=porcentajes_ingreso)])
            fig1.update_layout(title='Distribución de Ingresos por Tipo')

            # Crear el gráfico de torta para los egresos por tipo
            fig2 = go.Figure(data=[go.Pie(labels=tipos_egreso, values=porcentajes_egreso)])
            fig2.update_layout(title='Distribución de Egresos por Tipo')

            # Crear una figura con subplots de tipo "pie" para mostrar ambos gráficos
            fig = make_subplots(rows=1, cols=2, subplot_titles=['Ingresos', 'Egresos'], specs=[[{'type': 'pie'}, {'type': 'pie'}]])
            fig.add_trace(fig1.data[0], row=1, col=1)
            fig.add_trace(fig2.data[0], row=1, col=2)

            # Convertir la figura en un div HTML para renderizar en la plantilla
            plot_div = fig.to_html(full_html=False)

            # Crear el gráfico de barras dinámico para los ingresos por tipo
            # Crear el gráfico de barras dinámico para los ingresos por tipo
            bar_plot_div = crear_grafico_barras_dinamico(tipos_ingreso, montos_ingreso, 'Distribución de Ingresos por Tipo')
            bar_plot_div_eg = crear_grafico_barras_dinamico(tipos_egreso, montos_egreso, 'Distribución de Egresos por Tipo')

            total_ingreso_grupo = ingresos.aggregate(total=Sum('monto_ingreso'))['total']
            total_egreso_grupo = egresos.aggregate(total=Sum('monto_egreso'))['total']

            #subtotal = total_ingreso_grupo - total_egreso_grupo

            if total_ingreso_grupo is not None and total_egreso_grupo is not None:
                subtotal = total_ingreso_grupo - total_egreso_grupo
            else:
                subtotal = None  # O cualquier valor predeterminado que desees asignar cuando no haya valores disponibles
        return render(request, 'espacio.html', {'espacio': espacio, 'usuarios': usuarios,'creador':creador,'total_ing':total_ingreso_grupo,'total_eg':total_egreso_grupo,'subtotal':subtotal, 'plot_div': plot_div,'bar_plot_div': bar_plot_div,'bar_plot_div_eg':bar_plot_div_eg,'graph_json': graph_json,'form': form})

    else:
        form = EspacioForm()

        espacio = Espacio.objects.get(usuarios=request.user,id=espacio_id)
        creador = espacio.propietario.username
        usuarios = espacio.usuarios.all()
        print(type(creador))
        print(type(usuarios))

        colors = ['rgb(72, 199, 44)', 'rgb(220, 144, 31)', 'rgb(58, 104, 168)','rgb(147, 39, 210)']   # Ejemplo de lista de colores


        # Obtener todos los ingresos y egresos de los usuarios
        ingresos = Ingreso.objects.filter(hoja_informacion_financiera__propietario__in=usuarios)
        egresos = Egreso.objects.filter(hoja_informacion_financiera__propietario__in=usuarios)
        
        fuente_egreso_labels = []
        monto_egreso_values = []
        for egreso in egresos:
            fuente_egreso_labels.append(egreso.get_fuente_egreso_display())
            monto_egreso_values.append(float(egreso.monto_egreso))
        fig0 = go.Figure(data=[go.Bar(x=fuente_egreso_labels, y=monto_egreso_values,marker=dict(color=colors))])
        # Personaliza el diseño del gráfico
        fig0.update_layout(
            title="Montos asociados a fuente de egreso",
            xaxis_title="Fuente de egreso",
            yaxis_title="Monto de egreso",
        )
        # Convierte el gráfico en formato JSON
        graph_json = fig0.to_json()
        # Calcular el total de ingresos y egresos por tipo
        total_ingresos_tipo = ingresos.values('tipo_ingreso').annotate(total=Sum('monto_ingreso')).order_by('-total')
        total_egresos_tipo = egresos.values('tipo_egreso').annotate(total=Sum('monto_egreso')).order_by('-total')
        # Calcular el total de ingresos y egresos
        total_ingresos = ingresos.aggregate(total=Sum('monto_ingreso'))['total']
        total_egresos = egresos.aggregate(total=Sum('monto_egreso'))['total']
        # Crear una lista de tipos de ingreso y egreso
        tipos_ingreso = [ingreso['tipo_ingreso'] for ingreso in total_ingresos_tipo]
        tipos_egreso = [egreso['tipo_egreso'] for egreso in total_egresos_tipo]
        # Crear una lista de montos de ingreso y egreso
        montos_ingreso = [ingreso['total'] for ingreso in total_ingresos_tipo]
        montos_egreso = [egreso['total'] for egreso in total_egresos_tipo]
        # Calcular los porcentajes de ingresos y egresos
        porcentajes_ingreso = [(monto / total_ingresos) * 100 for monto in montos_ingreso]
        porcentajes_egreso = [(monto / total_egresos) * 100 for monto in montos_egreso]
        # Crear el gráfico de torta para los ingresos por tipo
        fig1 = go.Figure(data=[go.Pie(labels=tipos_ingreso, values=porcentajes_ingreso)])
        fig1.update_layout(title='Distribución de Ingresos por Tipo')
        # Crear el gráfico de torta para los egresos por tipo
        fig2 = go.Figure(data=[go.Pie(labels=tipos_egreso, values=porcentajes_egreso)])
        fig2.update_layout(title='Distribución de Egresos por Tipo')
        # Crear una figura con subplots de tipo "pie" para mostrar ambos gráficos
        fig = make_subplots(rows=1, cols=2, subplot_titles=['Ingresos', 'Egresos'], specs=[[{'type': 'pie'}, {'type': 'pie'}]])
        fig.add_trace(fig1.data[0], row=1, col=1)
        fig.add_trace(fig2.data[0], row=1, col=2)
        # Convertir la figura en un div HTML para renderizar en la plantilla
        plot_div = fig.to_html(full_html=False)
        # Crear el gráfico de barras dinámico para los ingresos por tipo
        # Crear el gráfico de barras dinámico para los ingresos por tipo
        bar_plot_div = crear_grafico_barras_dinamico(tipos_ingreso, montos_ingreso, 'Distribución de Ingresos por Tipo')
        bar_plot_div_eg = crear_grafico_barras_dinamico(tipos_egreso, montos_egreso, 'Distribución de Egresos por Tipo')
        total_ingreso_grupo = ingresos.aggregate(total=Sum('monto_ingreso'))['total']
        total_egreso_grupo = egresos.aggregate(total=Sum('monto_egreso'))['total']
        #subtotal = total_ingreso_grupo - total_egreso_grupo
        if total_ingreso_grupo is not None and total_egreso_grupo is not None:
            subtotal = total_ingreso_grupo - total_egreso_grupo
        else:
            subtotal = None  # O cualquier valor predeterminado que desees asignar cuando no haya valores disponibles
    return render(request, 'espacio.html', {'espacio': espacio, 'usuarios': usuarios,'creador':creador,'total_ing':total_ingreso_grupo,'total_eg':total_egreso_grupo,'subtotal':subtotal, 'plot_div': plot_div,'bar_plot_div': bar_plot_div,'bar_plot_div_eg':bar_plot_div_eg,'graph_json': graph_json,'form': form})



def crear_grafico_barras_dinamico(labels, values, title):
    
    colors = ['rgb(72, 199, 44)', 'rgb(220, 144, 31)', 'rgb(58, 104, 168)','rgb(147, 39, 210)']  # Ejemplo de lista de colores
    fig = go.Figure(data=[go.Bar(x=labels, y=values,marker=dict(color=colors))])
    fig.update_layout(title=title, xaxis_title='Categoría', yaxis_title='Valor')
    
    # Convertir la figura en un div HTML para renderizar en la plantilla
    plot_div = fig.to_html(full_html=False)
    
    # Devolver el div HTML del gráfico de barras
    return plot_div




def eliminar_usuario(request, espacio_id, usuario_id):
    # Obtener el objeto Espacio correspondiente al espacio_id
    espacio = Espacio.objects.get(id=espacio_id)
    # Obtener el usuario a eliminar
    usuario = UserProfile.objects.get(id=usuario_id).user
    # Eliminar el usuario del espacio
    espacio.usuarios.remove(usuario)
    return redirect('aplicacion:miEspacio')


def enviar_invitacion(request, espacio_id):
    if request.method == 'POST':
        espacio = Espacio.objects.get(id=espacio_id)
        correo = request.POST.get('correo')

        # Lógica para enviar la invitación por correo electrónico
        subject = 'Invitación a unirse al grupo'
        message = f'Hola,\n\nHas sido invitado por {request.user.username} a unirte al grupo "{espacio.nombre}".\n\n'
        message += f'Para registrarte   , visita el siguiente enlace: {request.build_absolute_uri(reverse("myapp:registro"))}\n\n'
        message += f'Código de invitación: {espacio.codigo_invitacion}\n\n'
        message += 'Esperamos verte pronto en nuestro grupo!\n\n'
        message += 'Saludos,\nEl equipo de ChauchaAPP'

        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [correo]

        send_mail(subject, message, from_email, recipient_list)

        # Realiza cualquier redireccionamiento o respuesta necesaria después de enviar la invitación
        return redirect('aplicacion:miEspacio', espacio_id=espacio_id)

    return redirect('aplicacion:index')





def eliminar_ingreso(request, ingreso_id):
    ingreso = Ingreso.objects.get(id=ingreso_id)
    ingreso.delete()
    return redirect('aplicacion:hoja_financiera')

def eliminar_egreso(request, egreso_id):
    egreso = Egreso.objects.get(id=egreso_id)
    egreso.delete()
    return redirect('aplicacion:hoja_financiera')


def abandonar_espacio(request,id_espacio):
    espacio = get_object_or_404(Espacio, id=id_espacio)
    espacio.usuarios.remove(request.user)
    espacio.save()
    return redirect('aplicacion:ver_espacios')


def disolver_espacio(request,id_espacio):
    espacio = get_object_or_404(Espacio, id=id_espacio)
    if request.user == espacio.propietario:
        espacio.delete()
        return redirect('aplicacion:ver_espacios')
    else:
        return redirect('aplicacion:ver_espacios')
