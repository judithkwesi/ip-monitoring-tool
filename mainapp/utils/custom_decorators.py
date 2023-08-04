from functools import wraps
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache

def custom_admin_only(view_func):
    # Apply the @never_cache decorator first to avoid caching the view
    view_func = never_cache(view_func)
    
    # Apply the @login_required decorator next
    view_func = login_required(login_url='login')(view_func)
    
    # Apply the @user_passes_test decorator with the is_superuser test
    view_func = user_passes_test(lambda u: u.is_superuser)(view_func)
    
    # Wrap the original view function to preserve its attributes
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    
    return wrapped_view


def custom_authorised_user(view_func):
    # Apply the @never_cache decorator first to avoid caching the view
    view_func = never_cache(view_func)
    
    # Apply the @login_required decorator next
    view_func = login_required(login_url='login')(view_func)
    
    # Wrap the original view function to preserve its attributes
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    
    return wrapped_view
