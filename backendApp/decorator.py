from django.http import HttpResponse
from functools import wraps
from django.shortcuts import render

def group_required(*group_names):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Check if the user is authenticated and if they are a superuser
            if not request.user.is_authenticated:
                return render(request, 'deny.html')
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Fetch all group names the user belongs to
            user_groups = set(request.user.groups.values_list('name', flat=True))
            # Check if user has any of the required groups
            if set(group_names).intersection(user_groups):
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'deny.html')
        return _wrapped_view
    return decorator

