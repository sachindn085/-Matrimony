from django.urls import path
from .views import *

urlpatterns = [
    path('',MessageCreateView.as_view(),name='create_message'),
    path('list/', MessageCreateView.as_view(), name='list_message'),
    path('delete/<int:message_id>', MessageDeleteView.as_view(), name='delete_message'),
    
]
    