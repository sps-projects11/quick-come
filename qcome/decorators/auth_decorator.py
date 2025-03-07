from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from functools import wraps

def auth_required(view_or_func=None, *, login_url='/login/admin/'):
    """
    Decorator to enforce authentication.
    Can be used on function-based and class-based views.
    
    Usage:
      @auth_required
      def my_view(request): ...
      
    or with a custom login URL:
    
      @auth_required(login_url='/custom/login/')
      class MyView(TemplateView): ...
    """
    def _auth_decorator(func):
        @wraps(func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(login_url)
            return func(request, *args, **kwargs)
        return _wrapped

    def decorator(view):
        if isinstance(view, type):
            view.dispatch = method_decorator(_auth_decorator)(view.dispatch)
            return view
        else:
            return _auth_decorator(view)
    
    if view_or_func is None:
        return decorator
    else:
        return decorator(view_or_func)

def role_required(view_or_func=None, *, login_url='/login/admin/'):
    """
    Decorator to enforce admin role (checks that request.user.is_staff is True).
    Can be used on function-based and class-based views.
    
    Usage:
      @role_required
      def my_admin_view(request): ...
      
    or on a class-based view:
    
      @role_required
      class MyAdminView(TemplateView): ...
    """
    def _role_decorator(func):
        @wraps(func)
        def _wrapped(request, *args, **kwargs):
            # If user is not an admin, log them out and redirect.
            if not request.user.is_staff:
                # Optionally, call logout(request) to clear the session.
                from django.contrib.auth import logout
                logout(request)
                return redirect(login_url)
            return func(request, *args, **kwargs)
        return _wrapped

    def decorator(view):
        if isinstance(view, type):
            view.dispatch = method_decorator(_role_decorator)(view.dispatch)
            return view
        else:
            return _role_decorator(view)
    
    if view_or_func is None:
        return decorator
    else:
        return decorator(view_or_func)
