from django.views import View
from qcome.services import user_service
from django.shortcuts import redirect,render

class ManageUsersListView(View):
    def get(self, request):
        users = user_service.get_all_user()
        return render(request, 'adminuser/user/user_list.html',{'users':users})
    

class ManageUsersCreateView(View):
    def get(self, request):
        return
    
    def post(self, request, user_id):
        return


class ManageUserProfile(View):
    def get(self , request, user_id):
        return
    
    def post(self, request, user_id):
        return
    
class ManageUserDelete(View):
    def post(self, request, user_id):
        return
    
