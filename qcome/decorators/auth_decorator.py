from functools import wraps
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from ..constants import Role  # adjust import as needed

def auth_required(view_or_func=None, *, login_url='/sign-in/'):
    """
    Decorator to enforce that the user is authenticated.
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


def role_required(*allowed_roles, page_type='default'):
    """
    Decorator to enforce role-based access.
    
    Parameters:
      *allowed_roles: The allowed role values.
      page_type: A string indicating the type of page being protected.
         Use 'admin' for admin pages and 'enduser' for normal end-user pages.
    
    Behavior:
      - For an admin page (page_type='admin'):
          If a user whose role is not in allowed_roles (e.g. an end-user)
          tries to access the page, they are logged out and redirected to
          the admin login page.
      - For an end-user page (page_type='enduser'):
          If a user whose role is not in allowed_roles (e.g. an admin)
          tries to access the page, they are logged out and redirected to
          the home page.
      - Otherwise, a fallback redirect is provided.
    
    Example usage:
    
      @role_required(Role.ADMIN.value, Role.SUPER_ADMIN.value, page_type='admin')
      class AdminHomeView(View):
          ...
      
      @role_required(Role.END_USER.value, page_type='enduser')
      class HomeView(View):
          ...
    """
    def _role_decorator(func):
        @wraps(func)
        def _wrapped(request, *args, **kwargs):
            user_role = request.user.roles  # assuming this holds an integer matching Role values
            if user_role in allowed_roles:
                return func(request, *args, **kwargs)
            else:
                if page_type == 'admin':
                    # For admin pages: if an end-user tries to access, log them out
                    # and redirect them to the admin login page.
                    if user_role == Role.END_USER.value:
                        logout(request)
                        return redirect('/login/admin/')
                    else:
                        # Fallback for unexpected roles
                        return redirect('/sign-up/')
                elif page_type == 'enduser':
                    # For end-user pages: if an admin (or super admin) tries to access,
                    # log them out and redirect them to the public home page.
                    if user_role in (Role.ADMIN.value, Role.SUPER_ADMIN.value):
                        logout(request)
                        return redirect('home')  # using the named URL "home"
                    else:
                        return redirect('/sign-up/')
                else:
                    return redirect('/sign-up/')
        return _wrapped

    def decorator(view):
        if isinstance(view, type):
            view.dispatch = method_decorator(_role_decorator)(view.dispatch)
            return view
        else:
            return _role_decorator(view)
    
    return decorator
