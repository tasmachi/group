from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.http import Http404, HttpResponse
from braces.views import SelectRelatedMixin
from . import models
from . import forms

# Create your views here.

User=get_user_model()

class PostList(SelectRelatedMixin,generic.ListView):
    model=models.Post
    template_name='posts/post_list.html'
    select_related=('user','group')

class UserPost(generic.ListView):
    model=models.Post
    template_name='posts/user_post_list.html'

    def get_queryset(self):
        username = self.kwargs.get('username')
        self.post_user = User.objects.prefetch_related('posts').get(username__iexact=username)
        return models.Post.objects.filter(user__username__iexact=username)
        
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['post_user']=self.post_user
        return context
    
class PostDetail(SelectRelatedMixin,generic.DeleteView):
    model=models.Post
    select_related=('user','group')

    def get_queryset(self):
        quesyset= super().get_queryset()
        return quesyset.filter(user__username__iexact=self.kwargs.get('username'))
    
class CreatePost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    fields=('message','group')
    model=models.Post

    def form_valid(self, form):
        self.object=form.save(commit=False)
        self.object.user=self.request.user
        self.object.save()
        return super().form_valid(form)
    
class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model=models.Post
    select_related=('user','group')
    success_url=reverse_lazy('posts:all')

    def get_queryset(self):
        queryset= super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)
    
    def delete(self,*args,**kwargs):
        messages.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)