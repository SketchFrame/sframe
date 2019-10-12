from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Notifications


@login_required
def viewNotifications(request):
    print(request.get_full_path())
    notifications = Notifications.objects.filter(user__user=request.user)
    unread = Notifications.objects.filter(
        Q(user__user=request.user) & Q(viewed=False))
    read = Notifications.objects.filter(
        Q(user__user=request.user) & Q(viewed=True) & Q(archieve=False))
    archive = Notifications.objects.filter(
        Q(user__user=request.user) & Q(viewed=True) & Q(archieve=True))
    return render(request, 'notifications/notifications.html', {
        'notifications': notifications,
        'unread': unread.count(),
        'read': read.count(),
        'archive': archive.count()
    })


@login_required
def archieve(request, pk):
    notification = Notifications.objects.get(
        Q(pk=pk) & Q(user__user=request.user))
    notification.archieve = True
    notification.viewed = True
    notification.save()
    messages.success(request, "Notification Archieved")
    return redirect('notification')


@login_required
def unarchieve(request, pk):
    notification = Notifications.objects.get(pk=pk)
    notification.archieve = False
    notification.save()
    messages.success(request, "Notification removed from archieved")
    return redirect('notification')


@login_required
def markAsRead(request, pk):
    notification = Notifications.objects.get(
        Q(pk=pk) & Q(user__user=request.user))
    notification.viewed = True
    notification.save()
    messages.success(request, "Marked as read")
    return redirect('notification')


@login_required
def markAllAsRead(request):
    Notifications.objects.filter(user__user=request.user).update(viewed=True)
    return redirect('notification')
