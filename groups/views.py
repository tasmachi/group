from typing import Any
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from .models import Group,GroupMember
from django.urls import reverse
from django.views import generic
from django.db import IntegrityError
from django.contrib import messages
# Create your views here.

class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields=('name','description')
    model=Group

    def get_success_url(self):
        return self.object.get_absolute_url()
    
class SingleGroup(generic.DetailView):
    model=Group

class ListGroup(generic.ListView):
    model=Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):
    

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
    
    def get(self,request,*args,**kwargs):
        group=get_object_or_404(Group,slug=self.kwargs.get('slug'))

        try:
         GroupMember.objects.create(user=self.request.user, group=group)
         messages.success(self.request, 'You have successfully joined the group!')
        except IntegrityError:  # Ensure to import IntegrityError
           messages.warning(self.request, 'You are already a member of this group.')
        
        return super().get(request,*args,**kwargs)

class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    
    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        return reverse('group:single',kwargs={'slug':self.kwargs.get('slug')})
    
    def get(self,request,*args,**kwargs):
        group=get_object_or_404(Group,slug=self.kwargs.get('slug'))
        try:
            membership= GroupMember.objects.get(user=self.request.user,group=group)
            membership.delete()
            messages.success(self.request,'You left the Group successfully!')
        except GroupMember.DoesNotExist:
            messages.warning(self.request, 'You are not a member of this group.')
        except Exception as e:
            messages.error(self.request, 'Something went wrong. Please try again.')
        
        return super().get(request,*args,**kwargs)