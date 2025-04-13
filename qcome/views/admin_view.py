from django.views import View
from django.shortcuts import render, redirect
from ..decorators import auth_required, role_required
from ..constants import Role, Gender
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages  # For user feedback
import datetime
from ..constants.error_message import ErrorMessage
from ..constants.success_message import SuccessMessage
from ..services import user_service, admin_service, workers_service, payment_service, booking_service
from qcome.package.file_management import save_uploaded_file
import json
from django.http import HttpResponseForbidden, HttpResponseBadRequest



class AdminCreateView(View):
    def get(self, request):
        # You could perform a redirect here, so the client gets to handle it as POST via JavaScript
        return render(request, 'adminuser/login/admin_create.html')  # The template triggers the POST

    def post(self, request):
        user = request.user

        if user.roles == Role.ADMIN.value:
            return HttpResponseForbidden("You are already an admin.")

        if not user_service.check_user_exist(user.email):
            return HttpResponseBadRequest("User does not exist.")

        try:
            user_service.admin_create(user)
        except Exception as e:
            return HttpResponseBadRequest(f"Failed to create admin: {str(e)}")
        
        messages.success(request, SuccessMessage.S00001.value)
        return redirect('myadmin')




class LoginAdminView(View):
    def get(self, request):
        return render(request, 'adminuser/login/login.html')
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')  # corrected field name

        # Authenticate the user. Adjust keyword if you're using email as username.
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.roles == Role.ADMIN.value:
                login(request, user)
                messages.success(request, SuccessMessage.S00001.value)
                return redirect('myadmin')  # Redirect to your admin home view; using named URL
            else:
                messages.error(request, ErrorMessage.E00011.value)
                return redirect('login_myadmin')
        else:
            messages.error(request, ErrorMessage.E00009.value)
            return redirect('login_myadmin')


class LoginOutAdminView(View):
    def get(self, request):
        logout(request)
        request.session.flush()  # Destroy session
        messages.success(request, SuccessMessage.S00014.value)
        return redirect("/login/admin/")


@auth_required(login_url='/login/admin/')
@role_required(Role.ADMIN.value, page_type='admin')
class AdminHomeView(View):
    def get(self, request):        
        admin_data = user_service.get_user(request.user.id)
        total_users = user_service.get_all_user().count()
        total_admins = user_service.get_all_admins().count()
        total_garages = user_service.get_all_garages().count()
        total_workers = workers_service.get_all_workers().count()
        total_revenue = payment_service.get_total_revenue()

        booking = booking_service.get_last_5_booking()

        weekly_booking_data = booking_service.get_weekly_booking_data()        
        
        monthly_user_data  = user_service.get_monthly_user_data()        

        data = {
            'total_users': total_users,
            'total_admins': total_admins,
            'total_garages': total_garages,
            'total_workers': total_workers,
            'total_revenue': total_revenue,
            'recent_bookings': booking,
            'weekly_booking_data': json.dumps(weekly_booking_data),
            'monthly_user_data': json.dumps(monthly_user_data)
        }

        return render(request, 'adminuser/home/dashboard.html', {'data':data, 'admin':admin_data})
    

@auth_required(login_url='/login/admin/')
@role_required(Role.ADMIN.value, page_type='admin')
class AdminProfileView(View):
    def get(self, request):
        admin_data = user_service.get_user(request.user.id)
        user = request.user    
        if user.gender:
            gender_name = Gender(user.gender).name.capitalize()  # e.g., "Male"
        else:
            gender_name = "Not provided"
        return render(request, 'adminuser/profile/profile.html',{'user':user, 'gender': gender_name, 'admin':admin_data,})
    
    
@auth_required(login_url='/login/admin/')
@role_required(Role.ADMIN.value, page_type='admin')
class AdminProfileUpdateView(View):
    def get(self, request):
        admin_data = user_service.get_user(request.user.id)
        return render(request, 'adminuser/profile/update_profile.html', {'admin': admin_data})

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
            profile_photo_path = save_uploaded_file(profile_photo, subfolder="profile-images")
        
        admin_service.admin_profile_update(
            user, first_name, middle_name, last_name, email, phone, gender, dob, profile_photo_path
        )

        messages.success(request, SuccessMessage.S00002.value)
        return redirect('myadmin_profile')
