from django.urls import path

from . import views

app_name='groups'

urlpatterns=[
    path('all-groups/',views.ListGroup.as_view(),name='all'),
    path('create-group/',views.CreateGroup.as_view(),name='create'),
    path('posts/in/<slug:slug>/',views.SingleGroup.as_view(),name='single'),
    path('member-join/<slug:slug>/',views.JoinGroup.as_view(),name='join'),
    path('member-leave/<slug:slug>/',views.LeaveGroup.as_view(),name='leave')
]