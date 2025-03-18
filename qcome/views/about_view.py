from django.views import View
from django.shortcuts import render, redirect


class AboutView(View):
    def get(self,request):
        return render(request, 'enduser/About/index.html')