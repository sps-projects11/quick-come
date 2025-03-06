from django.views import View
from django.shortcuts import render


class AdminHomeView(View):
    def get(self, request):
        return
    

class AsminDashboard(View):
    def get(self, request):
        return
    

class ManageUsersListView(View):
    def get(self, request):
        return
    

class ManageUserProfile(View):
    def get(self , request, user_id):
        return
    
    def post(self, request, user_id):
        return
    

class ManageServiceList(View):
    def get(self, request):
        return
    

class ManageServiceListCreate(View):
    def get(self, request):
        return
    
    def post(self, request):
        return

class ManageServiceListUpdate(View):
    def get(self, request, service_id):
        return


class ManageServiceListDelete(View):
    def post(self, request, service_id):
        return
    
        