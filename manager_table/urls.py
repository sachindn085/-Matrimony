from django.urls import path
from .views import *


urlpatterns= [
    path('',CommonMatchingListCreateView.as_view(), name='master'),
    path('by_id/<int:pk>',CommonMatchingRetrieveUpdateDestroyView.as_view(), name='master_by_id'),
    path('by_type/<str:religion>', GetMatchingView.as_view(), name='master_by_type'),
    path('add_sub/', SubscriptionTypeCreateView.as_view(), name='subscription_type'),
    path('update_sub/<int:pk>',SubscriptionTypeCreateView.as_view(),name='subscription_type_update'),
    path('list_sub/', SubscriptionTypeCreateView.as_view(), name='subscription_type_list'),
    path('delete_sub/<int:pk>', SubscriptionTypeCreateView.as_view(), name='subscription_type_delete'), 
]