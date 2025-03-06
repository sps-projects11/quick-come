import random
from django.contrib.auth import get_user_model, login, logout
from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.cache import cache
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

class UserRegistrationView(View):
    def get(self, request):
        """Render registration page."""
        return render(request, "register.html")

    def post(self, request):
        """Register user and request OTP."""
        phone = request.POST.get("phone")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        if User.objects.filter(username=phone).exists():
            return JsonResponse({"status": "error", "message": "Phone number already registered!"})

        user = User.objects.create(username=phone, first_name=first_name, last_name=last_name)
        request.session["phone"] = phone  # Store phone in session
        return JsonResponse({"status": "success", "message": "User registered! Request OTP."})


class RequestOTPView(View):
    def get(self, request):
        """Generate and send OTP."""
        phone = request.GET.get("phone")

        if not phone:
            return JsonResponse({"status": "error", "message": "Phone number is required!"})

        otp = random.randint(100000, 999999)  # Generate 6-digit OTP
        cache.set(f"otp_{phone}", otp, timeout=300)  # Store OTP for 5 minutes

        # Simulate sending OTP (replace with SMS API)
        print(f"OTP for {phone}: {otp}")  

        return JsonResponse({"status": "success", "message": "OTP sent successfully!"})


class RequestOTPView(View):
    def get(self, request):
        """Generate and send OTP."""
        phone = request.GET.get("phone")

        if not phone:
            return JsonResponse({"status": "error", "message": "Phone number is required!"})

        otp = random.randint(100000, 999999)  # Generate 6-digit OTP
        cache.set(f"otp_{phone}", otp, timeout=300)  # Store OTP for 5 minutes

        # Simulate sending OTP (replace with SMS API)
        print(f"OTP for {phone}: {otp}")  

        return JsonResponse({"status": "success", "message": "OTP sent successfully!"})


@method_decorator(csrf_exempt, name="dispatch")
class VerifyOTPView(View):
    def post(self, request):
        """Verify the OTP entered by the user."""
        phone = request.POST.get("phone")
        user_otp = request.POST.get("otp")

        if not phone or not user_otp:
            return JsonResponse({"status": "error", "message": "Phone and OTP required!"})

        saved_otp = cache.get(f"otp_{phone}")

        if saved_otp and str(saved_otp) == user_otp:
            cache.delete(f"otp_{phone}")  # Remove OTP after successful verification

            # Authenticate user and create session
            user, created = User.objects.get_or_create(username=phone)
            login(request, user)
            request.session["user_phone"] = phone  # Store phone in session

            return JsonResponse({"status": "success", "message": "OTP verified!", "redirect": "/home/"})
        else:
            return JsonResponse({"status": "error", "message": "Invalid OTP!"})


class ResendOTPView(View):
    def get(self, request):
        """Resend OTP to the user's phone number."""
        phone = request.GET.get("phone")

        if not phone:
            return JsonResponse({"status": "error", "message": "Phone number is required!"})

        # Generate new OTP
        otp = random.randint(100000, 999999)
        cache.set(f"otp_{phone}", otp, timeout=300)  # Store OTP for 5 minutes

        # Simulate sending OTP (replace with actual SMS API)
        print(f"Resent OTP for {phone}: {otp}")

        return JsonResponse({"status": "success", "message": "OTP resent successfully!"})


class LogoutView(View):
    def get(self, request):
        """Logout the user and clear session."""
        logout(request)
        request.session.flush()
        return redirect("/login/")
