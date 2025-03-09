from django.views import View
from django.shortcuts import render
from ..decorators import auth_required, role_required
from ..constants import Role
from ..services import get_user_details

@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class EnduserProfileView(View):
    def get(self, request):
        user_id=request.user.id
        return render(request,'enduser/user_profile.html',{'user':user_id})
    

class EnduserProfileCreate(View):
    def get(self, request):
        return
    




class EnduserProfileUpdate(View):
    def get(self, request, user_id):
        user_details = get_user_details(user_id)
        context = {'user_details': user_details}
        return render(request, 'enduser/profile/user_profile_update.html', context)


class EnduserProfileDelete(View):
    def post(self, request):
        return
    
#user_profile_update.html