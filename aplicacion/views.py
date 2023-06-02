from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import EspacioForm
from .models import Espacio

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