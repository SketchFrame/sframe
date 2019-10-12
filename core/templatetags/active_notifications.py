from django import template
from notifications.models import Notifications

register = template.Library()


@register.filter
def active_notifications(user):
    if user.is_authenticated:
        qs = Notifications.objects.filter(user__user=user, viewed=False)
        if qs.exists():
            print(qs.count())
            return qs.count()
    return False
