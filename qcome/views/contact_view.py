from django.views import View
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from ..constants.error_message import ErrorMessage
from ..constants.success_message import SuccessMessage
from qcome.services import workers_service, garage_service
from quickcome import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class ContactView(View):
    def get(self, request):
        is_worker = workers_service.is_user_a_garage_worker(request.user.id)
        is_garage = garage_service.is_user_a_garage_owner(request.user.id)
        if is_worker:
            return render(request, 'worker/Contact/index.html')
        elif is_garage:
            return render(request, 'garage/Contact/index.html')
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
                [settings.DEFAULT_FROM_EMAIL],
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
