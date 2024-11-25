from django.urls import path
from .views import *

urlpatterns =[
    path('buy/',SubscriptionView.as_view(),name='subscription'),
    path('view/', SubscriptionView.as_view(), name='subscription_view'),
    
]