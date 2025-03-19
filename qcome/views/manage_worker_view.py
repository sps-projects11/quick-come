from django.views import View
from django.shortcuts import render, redirect
from qcome.services import garage_service, user_service, workers_service
from django.http import JsonResponse
from django.contrib import messages 
from ..constants.error_message import ErrorMessage
from ..constants.success_message import SuccessMessage
from ..package.response import success_response,error_response
import os
import hashlib
from quickcome import settings


class ManageWorkerListView(View):
    def get(self, request):
        return render(request, 'manage_worker_list.html')
    

class ManageWorkerCreateView(View):
    def get(self, request):
        return render(request, 'manage_worker_create.html')
    
    def post(self, request):
        return redirect('manage_worker_list')
    

class ManageWorkerUpdateView(View):
    def get(self, request, worker_id):
        return render(request, 'manage_worker_update.html')
    
    def post(self, request, worker_id):
        return redirect('manage_worker_list')


class ManageWorkerToggleView(View):
    def post(self, request, worker_id):
        return redirect('manage_worker_list')