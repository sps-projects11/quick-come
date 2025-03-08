from django.views import View
from django.shortcuts import render
from ..decorators import auth_required, role_required
from ..constants import Role

class EnduserProfileView(View):
    @auth_required(login_url='/sign-in/')
    @role_required(Role.END_USER.value, page_type='enduser')
    def get(self, request):
        user_id=request.user.id
        return render(request,'enduser/user_profile.html',{'user':user_id})
    

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
    
