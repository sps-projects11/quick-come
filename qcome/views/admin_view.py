from django.views import View
from django.shortcuts import render, redirect
from ..decorators import auth_required, role_required
from ..constants import Role,Gender
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages  # For user feedback
import datetime
from ..constants.error_message import ErrorMessage
from ..constants.success_message import SuccessMessage
from ..services import user_service, admin_service

class LoginAdminView(View):
    def get(self, request):
        return render(request, 'adminuser/login/login.html')
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')  # corrected field name

        # Authenticate the user. Adjust keyword if you're using email as username.
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.roles in (Role.ADMIN.value, Role.SUPER_ADMIN.value):
                login(request, user)
                messages.success(request, SuccessMessage.S00001.value)
                return redirect('myadmin')  # Redirect to your admin home view; using named URL
                
            else:
                messages.error(request, ErrorMessage.E00001.value)
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
        return render(request, 'adminuser/home/index.html')

    
@auth_required(login_url='/login/admin/')
@role_required(Role.ADMIN.value, Role.SUPER_ADMIN.value, page_type='admin')
class AsminDashboard(View):
    def get(self, request):
        return render(request, 'adminuser/dashboard.html')
    

@auth_required(login_url='/login/admin/')
@role_required(Role.ADMIN.value, Role.SUPER_ADMIN.value, page_type='admin')
class AdminProfileView(View):
    def get(self, request):
        user = request.user    
        if user.gender:
            gender_name = Gender(user.gender).name.capitalize()  # e.g., "Male"
        else:
            gender_name = "Not provided"
        return render(request, 'adminuser/profile/profile.html',{'user':user, 'gender': gender_name})
    
    

@auth_required(login_url='/login/admin/')
@role_required(Role.ADMIN.value, Role.SUPER_ADMIN.value, page_type='admin')
class AdminPasswordUpdateView(View):
    def get(self, request):
        return
    


@auth_required(login_url='/login/admin/')
@role_required(Role.ADMIN.value, Role.SUPER_ADMIN.value, page_type='admin')
class AdminProfileUpdateView(View):
    def get(self, request):
        return render(request, 'adminuser/profile/update_profile.html')

    def post(self, request):
        auth_user = request.user
        first_name = request.POST.get('first_name', '').strip()
        middle_name = request.POST.get('middle_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        gender_str = request.POST.get('gender', '').strip()  # gender as string initially
        dob_str = request.POST.get('dob', '').strip()  # expected in YYYY-MM-DD format


        user = user_service.get_user(auth_user.id)
        print("POST data:", request.POST)
        gender = None
        if gender_str:
            try:
                gender = int(gender_str)
            except ValueError:
                gender = None

        # Convert dob string to date object if provided
        dob = None
        if dob_str:
            try:
                dob = datetime.datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, "Invalid date format for DOB. Please use YYYY-MM-DD.")
                return redirect('myadmin_profile')

        # Call your admin service to update the profile
        admin_service.admin_profile_update(
            user, first_name, middle_name, last_name, email, phone, gender, dob
        )
            
        messages.success(request, SuccessMessage.S00002.value)
        return redirect('myadmin_profile')

