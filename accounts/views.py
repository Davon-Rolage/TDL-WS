from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View

from .forms import CustomUserLoginForm


class LoginView(View):
    template_name = 'accounts/login.html'
    
    def get(self, request):
        form = CustomUserLoginForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
