from django.views import View
from django.shortcuts import render, redirect

class ContactView(View):
    def get(self,request):
        return render(request, 'enduser/Contact/index.html')