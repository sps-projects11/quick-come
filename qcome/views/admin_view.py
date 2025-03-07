from django.views import View
from django.shortcuts import render, redirect
from ..decorators import auth_required, role_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages  # For user feedback

class LoginAdminView(View):
    def get(self, request):
        return render(request, 'adminuser/login/login.html')
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')  # corrected field name

        # Authenticate the user. Adjust keyword if you're using email as username.
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('myadmin')  # Redirect to your admin home view; using named URL
            else:
                messages.error(request, "You do not have admin privileges.")
        else:
            messages.error(request, "Invalid email or password.")
        return redirect('login_myadmin')


        
class LoginOutAdminView(View):
    def get(self, request):
        logout(request)
        request.session.flush()  # Destroy session
        return redirect("/login/admin/")



@auth_required(login_url='/login/admin/')
@role_required(login_url='/login/admin/')
class AdminHomeView(View):
    def get(self, request):
        return render(request, 'adminuser/home/index.html')

    
@auth_required
class AsminDashboard(View):
    def get(self, request):
        return
    
