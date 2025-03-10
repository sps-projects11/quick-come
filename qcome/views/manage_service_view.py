from django.views import View
from django.shortcuts import render, redirect
from ..services import service_service 

class ManageServiceList(View):
    def get(self, request):
        service = service_service.service_List()
        print(service)
        return render(request, 'adminuser/service_catalog/service_catalog.html',{'services':service})
    

class ManageServiceListCreate(View):
    def get(self, request):
        return render(request, 'adminuser/service_catalog/service_catalog_from.html')
    
    def post(self, request):
        return

class ManageServiceListUpdate(View):
    def get(self, request, service_id):
        return


class ManageServiceListDelete(View):
    def post(self, request, service_id):
        return
    
        