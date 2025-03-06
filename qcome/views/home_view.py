from django.views import View
from django.http import HttpResponse
from django.shortcuts import render

class HomeView(View):
    def get(self, request):
        return render(request, 'enduser\home\index.html')
    
class UserSigninView(View):
    def get(self, request):
        return render(request, 'enduser\home\signup.html')
        
    def post(self, request):
        return
    
class ChangeMyThemeView(View):
    def post(self, request):
        return
        
