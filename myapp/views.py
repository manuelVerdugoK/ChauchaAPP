from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import RegistrationForm
from .models import UserProfile
from .forms import RegistrationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView


# Create your views here.
    

def index(request):
    return render(request,'Index/index.html')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = LoginForm
    def get_success_url(self):
        return reverse_lazy('aplicacion:index')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('myapp:verificacion', username=user.username)
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def verify(request, username):
    profile = UserProfile.objects.get(user__username=username)
    if request.method == 'POST':
        code = request.POST.get('code')
        if profile.verify_account(code):
            messages.success(request, 'Your account has been successfully verified.')
            return redirect('aplicacion:index')
        else:
            messages.error(request, 'Invalid verification code.')
    return render(request, 'registration/verify.html', {'username': username})