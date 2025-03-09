from django.views import View
from qcome.services import user_service
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import random
import time
from ..models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.hashers import check_password
from ..constants.error_message import ErrorMessage
from ..constants.success_message import SuccessMessage
from ..package.response import success_response,error_response



from django.contrib.auth import get_user_model
User = get_user_model()

# Store OTPs temporarily with expiry time
OTP_STORAGE = {}

class UserSignupView(View):
    def get(self,request):
        return render(request,  "enduser/home/signup.html")
    def post(self, request):
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        dob = request.POST.get("dob")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Password confirmation check
        if password != confirm_password:
            return JsonResponse({"status": "error", "message": "Passwords do not match."})

        # Check if email is verified
        if email not in OTP_STORAGE or not OTP_STORAGE[email]["verified"]:
            return JsonResponse({"status": "error", "message": "Email not verified."})

        # Save user
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            dob=dob,
            email=email,
            password=make_password(password)  # Hash password
        )
        del OTP_STORAGE[email]  # Remove OTP after successful registration
        return JsonResponse({"status": "success", "redirect": "/sign-in/"})


class RequestOTPView(View):
    def get(self, request):
        email = request.GET.get("email")
        if not email:
            return JsonResponse(error_response(ErrorMessage.E00003.value))
        
        if User.objects.filter(email=email).exists():
            return JsonResponse(error_response(ErrorMessage.E00004.value))

        otp = random.randint(100000, 999999)
        OTP_STORAGE[email] = {"otp": otp, "verified": False, "timestamp": time.time()}

        print(f"Your {email} OTP is: {otp}")

        send_mail(
            subject="Your OTP Code",
            message=f"Your OTP is: {otp}",
            from_email=settings.DEFAULT_FROM_EMAIL,  # Use Django settings
            recipient_list=[email],
            fail_silently=False,
        )

        msg = f"An OTP has been sent to {email}. Please check your email." # custom OTP Success Message
        
        return JsonResponse(success_response(msg), status=200)



class VerifyOTPView(View):
    def post(self, request):
        email = request.POST.get("email")
        otp = request.POST.get("otp")

        if email in OTP_STORAGE:
            stored_otp = OTP_STORAGE[email]["otp"]
            otp_timestamp = OTP_STORAGE[email]["timestamp"]

            if time.time() - otp_timestamp > 300:
                del OTP_STORAGE[email]
                return JsonResponse(error_response(ErrorMessage.E00005.value))

            if stored_otp == int(otp):
                OTP_STORAGE[email]["verified"] = True
                return JsonResponse(success_response(SuccessMessage.S00004.value))

        return JsonResponse(error_response(ErrorMessage.E00006.value))


class UserSigninView(View):
    def get(self, request):
        return render(request, "enduser/home/signin.html")

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        print("email:", email, "password:", password)

        try:
            user = User.objects.get(email=email)  # Get user by email
            if check_password(password, user.password):  # Check hashed password
                login(request, user)  # Log in user
                request.session["email"] = user.email  # Store email in session
                return JsonResponse({"status": "success", "redirect": "/"})
            else:
                return JsonResponse({"status": "error", "message": "Invalid email or password."})
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Invalid email or password."})



class UserLogoutView(View):
    def get(self, request):
        logout(request)
        request.session.flush()  # Destroy session
        return redirect("/sign-in/")
    





class PasswordResetView(View):
    def get(self, request):
        return render(request, 'enduser/home/password_reset.html')

    def post(self, request):
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User with this email does not exist."})

        # Generate password reset token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = f"{settings.SITE_URL}/password-reset-confirm/{uid}/{token}/"

        # Send reset email
        send_mail(
            subject="Password Reset Request",
            message=f"Click the link to reset your password: {reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return JsonResponse({"status": "success", "message": "Password reset link sent to your email."})


class PasswordResetConfirmView(View):
    def get(self, request, uidb64, token):
        return render(request, 'enduser/home/password_reset_confirm.html', {"uidb64": uidb64, "token": token})

    def post(self, request, uidb64, token):
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            return JsonResponse({"status": "error", "message": "Passwords do not match."})

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if not default_token_generator.check_token(user, token):
                return JsonResponse({"status": "error", "message": "Invalid or expired token."})

            user.password = make_password(new_password)
            user.save()

            return JsonResponse({"status": "success", "redirect": "/sign-in/"})

        except (User.DoesNotExist, ValueError, TypeError):
            return JsonResponse({"status": "error", "message": "Invalid reset link."})

class CheckLoginStatus(View):
    """Handles checking login status for authenticated users."""
    def get(self, request):
        if request.user.is_authenticated:
            return JsonResponse(user_service.get_user_profile(request.user.id))
        return JsonResponse({"logged_in": False, "profile_photo_url": None})
