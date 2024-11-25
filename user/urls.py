from django.urls import path
from django.urls import include
from .views import UserListView,UserDetailView,LoginView,UserCreateView,UserDeleteView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('register/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>', UserDetailView.as_view(), name='user-detail'),
    path('token/',LoginView.as_view(),name='login'),
    path('delete/<int:pk>', UserDeleteView.as_view(), name='user-delete')
    
]