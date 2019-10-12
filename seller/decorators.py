from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from users.models import UserExtended
from functools import wraps


def seller_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = UserExtended.objects.get(user__pk=request.user.id)
        if user.is_seller == True:
            return function(request, *args, **kwargs)
        else:
            return render(request, 'errors/403-access-forbidden.html')
    return wrap
