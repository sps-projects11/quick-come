from django.views import View
from qcome.services import user_service
from django.shortcuts import render,redirect,get_object_or_404
from ..decorators import auth_required, role_required
from ..constants import Role
from ..services import get_user_details,update_user_details,get_workers_details
import os
import hashlib
from django.conf import settings

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
    


class EnduserProfileUpdate(View):
    def get(self, request, user_id):
        user_details = get_user_details(user_id)
        context = {'user_details': user_details}
        return render(request, 'enduser/profile/user_profile_update.html', context)

    def post(self, request, user_id):
        user = get_user_details(user_id)
        if user:
            profile_photo = request.FILES.get('profile_picture')
            profile_photo_path = user.profile_photo_url  # Default to existing photo

            if profile_photo:
                profile_photo_img_dir = os.path.join(settings.BASE_DIR, 'static', 'all-Pictures')
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

                profile_photo_path = f'/static/all-Pictures/{new_file_name}'
                print("Updated profile photo path:", profile_photo_path)

            # ✅ Make a mutable copy of request.POST
            mutable_post = request.POST.copy()
            mutable_post['profile_photo_url'] = profile_photo_path  # Add new profile photo path

            update_user_details(user, mutable_post)  # Pass the modified request data
            return redirect('user_profile')

        return redirect('user_profile')



class EnduserProfileDelete(View):
    def get(self, request, user_id):
        user_details = get_user_details(user_id)
        context = {'user_details': user_details}
        return render(request, 'enduser/profile/user_profile_delete.html', context)

    def post(self, request, user_id):
        user = get_user_details(user_id)
        if user:
            user.delete()
            return redirect('user_profile')  
        return redirect('user_profile')


class WorkerCreateView(View):
    def get(self, request, worker_id):
        worker_details = get_workers_details(worker_id)
        context = {
            'worker_details': worker_details,
            'user': request.user,
        }
        return render(request, 'enduser/profile/garage_worker/worker_profile_create.html', context)

