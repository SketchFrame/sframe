from django import template
from users.models import UserExtended

register = template.Library()


@register.filter
def is_seller(user):
    if user.is_authenticated:
        qs = UserExtended.objects.filter(user=user, is_seller=True)
        if qs.exists():
            return True
    return False
