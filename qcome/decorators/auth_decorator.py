from functools import wraps
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from ..constants import Role  # adjust import as needed
from qcome.services import garage_service, workers_service
from django.contrib import messages  # For user feedback
from ..constants.error_message import ErrorMessage
from ..constants.success_message import SuccessMessage



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



def role_required(*allowed_roles, interface=None, page_type='default'):
    """
    Decorator to enforce role-based access control with optional interface checks for
    different end-user branches.

    Parameters:
      * allowed_roles (int): One or more role values (typically from the Role enum)
        that are permitted to access the view.
      * interface (str, optional): Specifies the branch of the end-user interface. 
          Valid values:
              'normal'  -> For a standard end-user interface.
              'garage'  -> For a garage owner interface.
              'worker'  -> For a garage worker interface.
          When provided (with page_type 'enduser'), the decorator will perform an additional
          check using service functions to verify the user belongs to the specified branch.
      * page_type (str, optional): Indicates the type of page being protected.
          Acceptable values:
              'admin'    -> For administrative pages.
              'enduser'  -> For end-user pages.
          Determines the redirection logic for unauthorized users.
    
    Behavior:
      1. Checks if the user's primary role (request.user.roles) is among the allowed_roles.
         - If not allowed:
             - For admin pages:
                 - If the user is an end-user, they are logged out and redirected to '/login/admin/'.
                 - Otherwise, they are redirected to '/sign-up/'.
             - For end-user pages:
                 - If the user is an admin or super admin, they are logged out and redirected
                   to the public home page (named URL "home").
                 - Otherwise, they are redirected to '/sign-up/'.
      2. For end-user pages (page_type == 'enduser') with an interface specified:
         - For interface 'garage': Verifies the user is a garage owner.
         - For interface 'worker': Verifies the user is a garage worker.
         - For interface 'normal': Ensures the user is not a garage owner or worker.
         - If the interface check fails, an error message is shown (for 'garage') and the user
           is logged out and redirected to '/sign-in/'.
      3. If all checks pass, the original view is executed.
    
    Returns:
      - The decorated view function (or class) with enforced role and interface checks.
    
    Usage:
      For a class-based view:
          @auth_required(login_url='/login/')
          @role_required(Role.END_USER.value, interface='garage', page_type='enduser')
          class GarageDashboardView(View):
              def get(self, request):
                  # view logic here
                  ...

      For a function-based view:
          @role_required(Role.END_USER.value, interface='worker', page_type='enduser')
          def worker_dashboard(request):
              # view logic here
              ...
    """
    def _role_decorator(func):
        @wraps(func)
        def _wrapped(request, *args, **kwargs):
            user_role = request.user.roles  # e.g. Role.END_USER.value
            
            # High-level role check.
            if user_role not in allowed_roles:
                # Admin page redirection logic.
                if page_type == 'admin':
                    if user_role == Role.END_USER.value:
                        logout(request)
                        return redirect('/login/admin/')
                    else:
                        return redirect('/sign-up/')
                # End-user page redirection logic.
                elif page_type == 'enduser':
                    if user_role in (Role.ADMIN.value, Role.SUPER_ADMIN.value):
                        logout(request)
                        return redirect('home')  # using the named URL "home"
                    else:
                        return redirect('/sign-up/')
                else:
                    return redirect('/sign-up/')
            
            # Additional branch/interface checks for end-user pages.
            if page_type == 'enduser' and interface:
                if interface == 'garage':
                    if not garage_service.is_user_a_garage_owner(request.user.id):
                        messages.error(request, ErrorMessage.E00011.value)
                        logout(request)
                        return redirect('/sign-in/')
                elif interface == 'worker':
                    if not workers_service.is_user_a_garage_worker(request.user.id):
                        logout(request)
                        return redirect('/sign-in/')
                elif interface == 'normal':
                    if (garage_service.is_user_a_garage_owner(request.user.id) or
                        workers_service.is_user_a_garage_worker(request.user.id)):
                        logout(request)
                        return redirect('/sign-in/')
            # If all checks pass, proceed to the view.
            return func(request, *args, **kwargs)
        return _wrapped

    def decorator(view):
        if isinstance(view, type):  # For class-based views.
            view.dispatch = method_decorator(_role_decorator)(view.dispatch)
            return view
        else:
            return _role_decorator(view)
    
    return decorator
