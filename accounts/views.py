from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from .models import User
from django.views.generic import CreateView,UpdateView,DeleteView,DetailView

# Create your views here.

class SignUp(CreateView):
    model=User
    form_class=forms.UserCreateForm
    success_url=reverse_lazy('home')
    template_name='accounts/signup.html'

    def form_valid(self, form):
        user=form.save()
        login(self.request,user)
        return redirect(self.success_url)
    
@login_required
def UserLogout(request):
    logout(request)
    return redirect('home')