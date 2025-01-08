from django.urls import path
from .views import NotificationView,SendBulkNotificationView,RetriveUnreadNotificationView

urlpatterns=[
    path('',NotificationView.as_view(),name="notification"),
    path('create/', SendBulkNotificationView.as_view(), name="notification_create"),
    path('unread/', RetriveUnreadNotificationView.as_view(), name="notification_unread")
    
]