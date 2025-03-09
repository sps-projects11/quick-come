from django.views import View
from qcome.services import user_service
from django.shortcuts import render
from ..decorators import auth_required, role_required
from ..constants import Role


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
        return
    
    def post(self, request, user_id):
        return
    

class EnduserProfileDelete(View):
    def post(self, request):
        return
    
