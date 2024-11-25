from django.urls import path
from .views import *

urlpatterns = [
    path('',MatchingCreateView.as_view(),name='create_matching'),
    path('list/', MatchingListView.as_view(), name='list_matching'),
    path('delete/<int:pk>/', MatchingListView.as_view(),name='delete_matching'),
    path('accept/<int:pk>/', MatchingUpdateView.as_view(), name='update_matching'),
    path('reject/<int:pk>/', MatchingRejectView.as_view(), name='reject_matching'),
    path('matchings/', MatchingRetriveView.as_view(),name='get_matchings'),

]