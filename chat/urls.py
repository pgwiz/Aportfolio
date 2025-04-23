from django.urls import path
from .views import (
    MessageListView,
    MessageDetailView,
    NotificationListView,
    MarkNotificationSeenView
)

urlpatterns = [
    path('messages/', MessageListView.as_view(), name='message-list'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/seen/', MarkNotificationSeenView.as_view(), name='mark-notification-seen'),
]