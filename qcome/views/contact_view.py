from django.views import View
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from ..constants.error_message import ErrorMessage
from ..constants.success_message import SuccessMessage

class ContactView(View):
    def get(self, request):
        return render(request, 'enduser/Contact/index.html')
    
    def post(self, request):
        try:
            email = request.POST.get("contacter_email")
            subject = request.POST.get("contacter_subject")
            msg = request.POST.get("contacter_msg")
            
            email_msg = EmailMultiAlternatives(
                subject,
                msg,
                email,
                ['sps.projects1010@gmail.com'],
            )
            
            email_msg.reply_to = [email]
            email_msg.send()

            messages.success(request, SuccessMessage.S00015.value)
            return redirect("home")
        except Exception as e:
            # Log the error for debugging purposes
            print("Error sending email:", e)
            messages.error(request, ErrorMessage.E00020.value)
            return redirect("home")
