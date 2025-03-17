from django.views import View
from django.shortcuts import render, redirect
from qcome.services import garage_service, user_service
from ..constants.error_message import ErrorMessage
from ..constants.success_message import SuccessMessage
from ..package.response import success_response,error_response
from django.http import JsonResponse

class ManageGarageListView(View):
    def get(self, request):
        garages = garage_service.get_garage_list()

        return render(request, 'adminuser/garage/garage_list.html', {'garages':garages})
    
class ManageGarageCreateView(View):
    def get(self, request):
        # is_not_garage = user_service.get_all_user_who_are_not_garage_owner()

        # return render(request, '')
        return
    def post(self, requset):
        return
    
class ManageGarageUpdateView(View):
    def get(self, request, garage_id):
        return
    def post(self, request, garage_id):
        return
    

class ManageGarageToggleView(View):
    def post(self, request, garage_id):
        garage = garage_service.toggle_garage_status(garage_id)

        if garage is None:
            return JsonResponse(error_response(ErrorMessage.E00013.value))
        
        return JsonResponse(success_response(SuccessMessage.S00006.value))