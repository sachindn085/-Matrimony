from django.urls import path
from .views import *

urlpatterns = [
    path('',CreatePreferenceView.as_view(), name='preference'),
    path('delete/', UpdateDeleteView.as_view(),name='preference_update'),
    path('update/', UpdateDeleteView.as_view(), name='preference_update')

]