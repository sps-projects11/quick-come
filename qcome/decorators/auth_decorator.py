from functools import wraps
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.http import HttpRequest
from ..constants import Role  # adjust import as needed
from qcome.services import garage_service, workers_service
from django.contrib import messages  # For user feedback
from ..constants.error_message import ErrorMessage
from ..constants.success_message import SuccessMessage


def auth_required(view_or_func=None, *, login_url='/sign-in/'):
    """
    Decorator to ensure the user is authenticated.
    
    Automatically detects if the decorated callable is a function-based view or a 
    method on a class-based view.
    
    If the user is not authenticated, they are redirected to the login URL.
    
    Usage:
      @auth_required(login_url='/sign-in/')
      def my_view(request):
          ...

      or

      @auth_required(login_url='/sign-in/')
      class MyView(View):
          def get(self, request, *args, **kwargs):
              ...
    """
    def _auth_decorator(func):
        @wraps(func)
        def _wrapped(*args, **kwargs):
            # Auto-detect the HttpRequest object.
            if args and isinstance(args[0], HttpRequest):
                request = args[0]
            elif len(args) > 1 and isinstance(args[1], HttpRequest):
                request = args[1]
            else:
                raise ValueError("Could not determine the request object in auth_required decorator.")

            if not request.user.is_authenticated:
                return redirect(login_url)
            return func(*args, **kwargs)
        return _wrapped

    def decorator(view):
        if isinstance(view, type):  # Class-based view.
            view.dispatch = method_decorator(_auth_decorator)(view.dispatch)
            return view
        else:  # Function-based view.
            return _auth_decorator(view)
    
    if view_or_func is None:
        return decorator
    else:
        return decorator(view_or_func)


def role_required(*allowed_roles, interface=None, page_type='default'):
    """
    Decorator to enforce role-based access control with optional interface checks
    for different end-user branches.
    
    Parameters:
      allowed_roles (int): One or more role values (from the Role enum) that are permitted
                           to access the view.
      interface (str, optional): Specifies the branch of the end-user interface.
                                 Valid values:
                                   'normal'  -> Standard end-user interface.
                                   'garage'  -> Garage owner interface.
                                   'worker'  -> Garage worker interface.
      page_type (str, optional): Indicates the type of page being protected.
                                 Valid values:
                                   'admin'   -> Administrative pages.
                                   'enduser' -> End-user pages.
    
    Behavior:
      1. Checks if the user's primary role (request.user.roles) is in allowed_roles.
         - If not:
             - For admin pages:
                 - Logs out end-users and redirects to '/login/admin/'.
                 - Otherwise, redirects to '/sign-up/'.
             - For end-user pages:
                 - Logs out admins/super admins and redirects to the public home page.
                 - Otherwise, redirects to '/sign-up/'.
      2. For end-user pages with an interface specified:
         - For 'garage': Verifies the user is a garage owner.
         - For 'worker': Verifies the user is a garage worker.
         - For 'normal': Ensures the user is neither a garage owner nor a worker.
         - On failure, an error message may be shown, the user is logged out, and they are
           redirected to '/sign-in/'.
      3. If all checks pass, the original view is executed.
    
    Automatically adapts to function-based views or class-based views.
    
    Usage:
      @auth_required(login_url='/sign-in/')
      @role_required(Role.END_USER.value, interface='garage', page_type='enduser')
      class PaymentListView(View):
          def get(self, request, *args, **kwargs):
              # View logic here.
              ...

      or

      @auth_required(login_url='/sign-in/')
      @role_required(Role.END_USER.value, interface='worker', page_type='enduser')
      def worker_payment_view(request):
          # View logic here.
          ...
    """
    def _role_decorator(func):
        @wraps(func)
        def _wrapped(*args, **kwargs):
            # Auto-detect the HttpRequest object.
            if args and isinstance(args[0], HttpRequest):
                request = args[0]
            elif len(args) > 1 and isinstance(args[1], HttpRequest):
                request = args[1]
            else:
                raise ValueError("Could not determine the request object in role_required decorator.")

            user_role = request.user.roles  # e.g. Role.END_USER.value

            # High-level role check.
            if user_role not in allowed_roles:
                if page_type == 'admin':
                    if user_role == Role.END_USER.value:
                        logout(request)
                        return redirect('/login/admin/')
                    else:
                        return redirect('/sign-up/')
                elif page_type == 'enduser':
                    if user_role in (Role.ADMIN.value, Role.SUPER_ADMIN.value):
                        logout(request)
                        return redirect('home')  # Named URL for home.
                    else:
                        return redirect('/sign-up/')
                else:
                    return redirect('/sign-up/')

            # Additional branch/interface checks for end-user pages.
            if page_type == 'enduser' and interface:
                if interface == 'garage':
                    if not garage_service.is_user_a_garage_owner(request.user.id):
                        messages.error(request, ErrorMessage.E00011.value)
                        return redirect('/garage/create/')
                    
                elif interface == 'worker':
                    if not workers_service.is_user_a_garage_worker(request.user.id):
                        messages.error(request, ErrorMessage.E00011.value)
                        return redirect(f'/worker/{request.user.id}/create/')
                    
                elif interface == 'normal':
                    if (garage_service.is_user_a_garage_owner(request.user.id) or
                        workers_service.is_user_a_garage_worker(request.user.id)):
                        messages.error(request, ErrorMessage.E00011.value)
                        logout(request)
                        return redirect('/sign-in/')
                    
            return func(*args, **kwargs)
        return _wrapped

    def decorator(view):
        if isinstance(view, type):  # Class-based view.
            view.dispatch = method_decorator(_role_decorator)(view.dispatch)
            return view
        else:
            return _role_decorator(view)
    
    return decorator


def garage_required(view_or_func=None, *, login_url='/sign-in/'):
    decorator = role_required(Role.END_USER.value, interface='garage', page_type='enduser')
    if view_or_func:
        return auth_required(login_url=login_url)(decorator(view_or_func))
    return lambda view: auth_required(login_url=login_url)(decorator(view))


def worker_required(view_or_func=None, *, login_url='/sign-in/'):
    decorator = role_required(Role.END_USER.value, interface='worker', page_type='enduser')
    if view_or_func:
        return auth_required(login_url=login_url)(decorator(view_or_func))
    return lambda view: auth_required(login_url=login_url)(decorator(view))
