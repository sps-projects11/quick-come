from django.views import View
from django.shortcuts import render, redirect
from ..decorators import auth_required, role_required
from ..constants import Role
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages  # For user feedback
import datetime
from ..constants import success_message
from ..constants import error_message

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
@role_required(Role.ADMIN.value, Role.SUPER_ADMIN.value, page_type='admin')
class AdminHomeView(View):
    def get(self, request):
        user = request.user
        return render(request, 'adminuser/home/index.html',{user:'user'})

    
@auth_required
class AsminDashboard(View):
    def get(self, request):
        return render(request, 'adminuser/dashboard.html')
    

class AdminProfileView(View):
    def get(self, request):
        return render(request, 'adminuser/profile/profile.html')

class AdminPasswordUpdateView(View):
    def get(self, request):
        return
    

class AdminProfileUpdateView(View):
    def get(self, request):
        return render(request, 'adminuser/profile/update_profile.html')

    def post(self, request):
        user = request.user
        first_name = request.POST.get('first_name', '').strip()
        middle_name = request.POST.get('middle_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        gender = request.POST.get('gender', '').strip()
        dob = request.POST.get('dob', '').strip()

        messages.success(request, "Profile updated successfully.")
        return redirect('myadmin_profile')
