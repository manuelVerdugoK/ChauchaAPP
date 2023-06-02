from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import EspacioForm,IngresoForm,EgresoForm
from .models import Espacio,Ingreso,HojaInformacionFinanciera,Egreso

import plotly.graph_objs as go
from plotly.subplots import make_subplots


from django.db.models import Sum
import matplotlib.pyplot as plt 


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
            return render(request,'index.html',{'form': form})
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



def mi_espacio(request):
    espacio = Espacio.objects.get(usuarios=request.user)
    usuarios = espacio.usuarios.all()

    # Obtener todos los ingresos y egresos de los usuarios
    ingresos = Ingreso.objects.filter(hoja_informacion_financiera__propietario__in=usuarios)
    egresos = Egreso.objects.filter(hoja_informacion_financiera__propietario__in=usuarios)

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

    

    return render(request, 'espacio.html', {'espacio': espacio, 'usuarios': usuarios, 'plot_div': plot_div,'bar_plot_div': bar_plot_div})


def crear_grafico_barras_dinamico(labels, values, title):
    fig = go.Figure(data=[go.Bar(x=labels, y=values)])
    fig.update_layout(title=title, xaxis_title='Categoría', yaxis_title='Valor')
    
    # Convertir la figura en un div HTML para renderizar en la plantilla
    plot_div = fig.to_html(full_html=False)
    
    # Devolver el div HTML del gráfico de barras
    return plot_div










