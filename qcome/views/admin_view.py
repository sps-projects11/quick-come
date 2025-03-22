from django.views import View
from django.shortcuts import render, redirect
from ..decorators import auth_required, role_required
from ..constants import Role,Gender
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages  # For user feedback
import datetime
from ..constants.error_message import ErrorMessage
from ..constants.success_message import SuccessMessage
from ..services import user_service, admin_service, garage_service, workers_service, payment_service, booking_service, service_service
import os
import hashlib
from django.conf import settings


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
        user = user_service.get_user(request.user.id)
        total_users = user_service.get_all_user().count()
        total_admins = user_service.get_all_admins().count()
        total_garages = garage_service.get_all_garages().count()
        total_workers = workers_service.get_all_workers().count()
        total_revenue = payment_service.get_total_revenue()

        booking = booking_service.get_last_5_booking()

        total_booking_by_week = booking_service.get_total_booking_by_week()

        print(total_booking_by_week)
        
        # total_user_by_month = user_service.get_total_user_by_month()

        # print(total_user_by_month)

        data = {
            'total_users': total_users,
            'total_admins': total_admins,
            'total_garages': total_garages,
            'total_workers': total_workers,
            'total_revenue': total_revenue,
            'admin': user
        }

        return render(request, 'adminuser/home/dashboard.html', {'data':data})
    

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
        return render(request, 'adminuser/login/forgot_password.html')
    def post(self, request):
        return


@auth_required(login_url='/login/admin/')
@role_required(Role.ADMIN.value, Role.SUPER_ADMIN.value, page_type='admin')
class AdminProfileUpdateView(View):
    def get(self, request):
        return render(request, 'adminuser/profile/update_profile.html')

    def post(self, request):
        auth_user = request.user
        user = user_service.get_user(auth_user.id)

        # Fetch form data and strip whitespace
        first_name = request.POST.get('first_name').strip() or user.first_name
        middle_name = request.POST.get('middle_name').strip() or None
        last_name = request.POST.get('last_name').strip() or user.last_name
        email = request.POST.get('email').strip() or user.email
        phone = request.POST.get('phone').strip() or user.phone
        gender_str = request.POST.get('gender')
        dob_str = request.POST.get('dob') or user.dob

        gender = user.gender
        if gender_str:
            gender = int(gender_str)
                
        if dob_str:
            try:
                dob = datetime.datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, ErrorMessage.E00002.value)
                return redirect('myadmin_profile')

        # Profile photo handling
        profile_photo = request.FILES.get('profile_photo')
        profile_photo_path = user.profile_photo_url

        if profile_photo:
            profile_photo_img_dir = os.path.join(settings.BASE_DIR, 'static', 'all-Pictures', 'profile-images')
            if not os.path.exists(profile_photo_img_dir):
                os.makedirs(profile_photo_img_dir)

            md5_hash = hashlib.md5()
            for chunk in profile_photo.chunks():
                md5_hash.update(chunk)
            file_hash = md5_hash.hexdigest()

            _, ext = os.path.splitext(profile_photo.name)
            new_file_name = f"{file_hash}{ext}"
            file_path = os.path.join(profile_photo_img_dir, new_file_name)

            if not os.path.exists(file_path):
                profile_photo.seek(0)
                with open(file_path, 'wb+') as destination:
                    for chunk in profile_photo.chunks():
                        destination.write(chunk)

            profile_photo_path = f'/static/all-Pictures/profile-images/{new_file_name}'

        
        admin_service.admin_profile_update(
            user, first_name, middle_name, last_name, email, phone, gender, dob, profile_photo_path
        )

        messages.success(request, SuccessMessage.S00002.value)
        return redirect('myadmin_profile')
