from django.views import View
from qcome.services import user_service
from django.shortcuts import render,redirect
from ..decorators import auth_required, role_required
from ..constants import Role
from ..services import get_user_details,update_user_details
from django.core.files.storage import FileSystemStorage


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
            profile_picture = request.FILES.get('profile_picture')
            if profile_picture:
                fs = FileSystemStorage(location='static/profile_pictures')
                filename = fs.save(profile_picture.name, profile_picture)
                profile_photo_url = fs.url(filename)
                request.POST = request.POST.copy()
                request.POST['profile_photo_url'] = profile_photo_url

            update_user_details(user, request.POST)
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
