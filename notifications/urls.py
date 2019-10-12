from django.urls import path, include
from .views import (
    # view_archieved_notifications
    viewNotifications,
    archieve,
    unarchieve,
    markAsRead,
    markAllAsRead
)

urlpatterns = [
    path('', viewNotifications, name="notification"),
    path('<int:pk>/archieve/', archieve, name="archieve"),
    path('<int:pk>/unarchieve/', unarchieve, name="unarchieve"),
    path('<int:pk>/mark-as-read/', markAsRead, name="mark-as-read"),
    path('mark-all-as-read/', markAllAsRead, name="mark-all-as-read"),
]
