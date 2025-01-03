from django.urls import path
from. import views

app_name='posts'

urlpatterns=[
    path('',views.PostList.as_view(),name='all'),
    path('create-post/',views.CreatePost.as_view(),name='create'),
    path('by/<username>/',views.UserPost.as_view(),name='for-user'),
    path('by/<username>/<int:pk>/',views.PostDetail.as_view(),name='single'),
    path('delete/<int:pk>/',views.DeletePost.as_view(),name='delete')
]