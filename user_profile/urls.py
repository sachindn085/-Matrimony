from django.urls import path
from .views import *


urlpatterns=[
    path('',ProfileListCreateView.as_view(), name='profile'),
    path('create/', ProfileUpdateView.as_view(), name='profile_create'),
    path('get/', ProfileUpdateView.as_view(), name='profile_get'),
    path('update/',UpdateView.as_view(), name='profile_update'),
    path('delete/', UpdateView.as_view(), name='profile_delete'),
   
]