from django.http import JsonResponse
from django.views import View
from qcome.services import user_service
from django.shortcuts import redirect,render
import os
import hashlib
from quickcome import settings
from ..constants.error_message import ErrorMessage
from ..constants.success_message import SuccessMessage
from ..package.response import success_response,error_response

class ManageUsersListView(View):
    def get(self, request):
        users = user_service.get_all_user()
        return render(request, 'adminuser/user/user_list.html',{'users':users})
    

class ManageUsersCreateView(View):
    def get(self, request):
        return render(request, 'adminuser/user/create_user.html')
    
    def post(self, request):
        print(request.POST)
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender') or None
        
        # Profile photo handling
        profile_photo = request.FILES.get('profile_photo')
        profile_photo_path = ''

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
        
        user_service.user_create(first_name, middle_name, last_name, dob, email, phone, gender, profile_photo_path)

        return redirect('manage_users')


class ManageUserUpdateView(View):
    def get(self , request, user_id):
        return
    
    def post(self, request, user_id):
        return
    

class ManageUserToggleView(View):
    def post(self, request, user_id):
        # Toggle the user's status using the service function.
        user = user_service.toggle_user_status(user_id)
        if user is None:
            return JsonResponse(error_response(ErrorMessage.E00012.value))
        # Return the updated status in JSON format.
        return JsonResponse(success_response(SuccessMessage.S00005.value))

    
