from django.views import View
from qcome.services import user_service
from django.shortcuts import render,redirect
from ..decorators import auth_required, role_required
from ..constants import Role
import os
import hashlib
from django.conf import settings
from django.contrib import messages
from ..constants.success_message import SuccessMessage

@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class EnduserProfileView(View):
    def get(self, request):
        user_id=request.user.id
        user_details=user_service.get_user_details(user_id)
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
                profile_photo_img_dir = os.path.join(settings.BASE_DIR, 'static', 'all-Pictures', 'profile-images')
                os.makedirs(profile_photo_img_dir, exist_ok=True)  # Ensure the directory exists

                # Generate unique file name using MD5 hash
                md5_hash = hashlib.md5()
                for chunk in profile_photo.chunks():
                    md5_hash.update(chunk)
                file_hash = md5_hash.hexdigest()

                _, ext = os.path.splitext(profile_photo.name)
                new_file_name = f"{file_hash}{ext}"
                file_path = os.path.join(profile_photo_img_dir, new_file_name)

                # Save file only if it does not exist
                if not os.path.exists(file_path):
                    profile_photo.seek(0)
                    with open(file_path, 'wb+') as destination:
                        for chunk in profile_photo.chunks():
                            destination.write(chunk)

                profile_photo_path = f'/static/all-Pictures/profile-images/{new_file_name}'
                print("Updated profile photo path:", profile_photo_path)

            # ✅ Make a mutable copy of request.POST
            mutable_post = request.POST.copy()
            mutable_post['profile_photo_url'] = profile_photo_path  # Add new profile photo path

            user_service.update_user_details(user, mutable_post)  # Pass the modified request data
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






        




