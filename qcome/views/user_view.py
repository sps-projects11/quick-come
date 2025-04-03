from django.views import View
from qcome.services import user_service,workers_service,garage_service
from django.shortcuts import render,redirect
from ..decorators import auth_required, role_required
from ..constants import Role
from django.contrib import messages
from ..constants.success_message import SuccessMessage
from ..constants.error_message import ErrorMessage
from qcome.package.file_management import save_uploaded_file

@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class EnduserProfileView(View):
    def get(self, request):
        user_id=request.user.id
        user_details=user_service.get_user_details(user_id)
        is_worker=workers_service.is_user_a_garage_worker(user_id)
        is_garage=garage_service.is_user_a_garage_owner(user_id)
        if is_garage:
           return redirect('/garage/profile/') 
        if is_worker:
            return redirect('/worker/')
        return render(request,'enduser/Profile/user_profile.html',{'user':user_details})
        
    

class EnduserProfileCreate(View):
    def get(self, request):
        return
    

@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class EnduserProfileUpdate(View):
    def get(self, request, user_id):
        user_details = user_service.get_user_details(user_id)
        context = {'user_details': user_details}
        return render(request, 'enduser/profile/user_profile_update.html', context)

    def post(self, request, user_id):
        user = user_service.get_user_details(user_id)
        if user:
            profile_photo = request.FILES.get('profile_picture')

            profile_photo_path = user.profile_photo_url  # Default to existing photo
                    
            if profile_photo:
                profile_photo_path = save_uploaded_file(profile_photo, subfolder="profile-images")
                print("Updated profile photo path:", profile_photo_path)

            # ✅ Make a mutable copy of request.POST
            mutable_post = request.POST.copy()
            mutable_post['profile_photo_url'] = profile_photo_path  # Add new profile photo path

            user_service.update_user_details(user, mutable_post)  # Pass the modified request data
            messages.success(request, SuccessMessage.S00020.value)
            return redirect('user_profile')
        messages.success(request, SuccessMessage.S00020.value)
        return redirect('user_profile')


@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class EnduserProfileDelete(View):
    def post(self, request, user_id):
        user = user_service.get_user_details(user_id)
        if user:
            user.delete()
            messages.success(request, SuccessMessage.S00021.value)
            return redirect('home')  
        return redirect('home')






        




