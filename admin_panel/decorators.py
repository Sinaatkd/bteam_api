from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

from functools import wraps

def check_group(group_name):
    def _check_group(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_anonymous:
                return redirect('/admin/')
            if not (request.user.groups.filter(name=group_name).exists()):
                raise PermissionDenied()
            return view_func(request, *args, **kwargs)
        return wrapper
    return _check_group