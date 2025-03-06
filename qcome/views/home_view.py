from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import random
import time
from ..models import User

class HomeView(View):
    def get(self, request):
        return render(request, 'enduser\home\index.html')

# Store OTPs temporarily with expiry time
OTP_STORAGE = {}

class UserSignupView(View):
    def get(self, request):
        return render(request, "enduser/home/signup.html")

    def post(self, request):
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        dob = request.POST.get("dob")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return JsonResponse({"status": "error", "message": "Passwords do not match."})

        if email not in OTP_STORAGE or not OTP_STORAGE[email]["verified"]:
            return JsonResponse({"status": "error", "message": "Email not verified."})

        user = User(
            username=email,  # Set username as email
            first_name=first_name,
            last_name=last_name,
            dob=dob,
            email=email
        )
        user.set_password(password)  # Hash password
        user.save()

        del OTP_STORAGE[email]  # Remove OTP after successful registration
        return JsonResponse({"status": "success", "redirect": "/sign-in/"})

class RequestOTPView(View):
    def get(self, request):
        email = request.GET.get("email")
        if not email:
            return JsonResponse({"status": "error", "message": "Email required."})

        otp = random.randint(100000, 999999)
        OTP_STORAGE[email] = {"otp": otp, "verified": False, "timestamp": time.time()}

        send_mail(
            subject="Your OTP Code",
            message=f"Your OTP is: {otp}",
            from_email=settings.DEFAULT_FROM_EMAIL,  # Use Django settings
            recipient_list=[email],
            fail_silently=False,
        )

        return JsonResponse({"status": "success", "message": "OTP sent to your email."})

class VerifyOTPView(View):
    def post(self, request):
        email = request.POST.get("email")
        otp = request.POST.get("otp")

        if email in OTP_STORAGE:
            stored_otp = OTP_STORAGE[email]["otp"]
            otp_timestamp = OTP_STORAGE[email]["timestamp"]

            if time.time() - otp_timestamp > 300:
                del OTP_STORAGE[email]
                return JsonResponse({"status": "error", "message": "OTP expired. Please request a new one."})

            if stored_otp == int(otp):
                OTP_STORAGE[email]["verified"] = True
                return JsonResponse({"status": "success", "message": "OTP verified."})

        return JsonResponse({"status": "error", "message": "Invalid OTP."})

class UserSigninView(View):
    def get(self, request):
        return render(request, "enduser/home/signin.html")

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            request.session["email"] = user.email  # Store email in session
            return JsonResponse({"status": "success", "redirect": "/home/"})
        else:
            return JsonResponse({"status": "error", "message": "Invalid email or password."})

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        request.session.flush()  # Destroy session
        return redirect("/sign-in/")

    
class ChangeMyThemeView(View):
    def post(self, request):
        return
        
