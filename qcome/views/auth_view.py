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
from django.contrib.auth.hashers import check_password
from ..constants.error_message import ErrorMessage
from ..constants.success_message import SuccessMessage
from ..package.response import success_response,error_response
from django.contrib import messages  # For user feedback
import json
from ..decorators import auth_required, role_required
from qcome.constants.default_values import Role
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


from django.contrib.auth import get_user_model
User = get_user_model()

# Store OTPs temporarily with expiry time
OTP_STORAGE = {}

@method_decorator(csrf_exempt, name='dispatch')
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
        hash_password=make_password(password)  # Hash password

        # Password confirmation check
        if password != confirm_password:
            return JsonResponse(error_response(ErrorMessage.E00007.value))

        # Check if email is verified
        if email not in OTP_STORAGE or not OTP_STORAGE[email]["verified"]:
            return JsonResponse(error_response(ErrorMessage.E00008.value))
        
        user = user_service.create_user_initially(first_name, last_name, dob, email, hash_password)
        del OTP_STORAGE[email]  # Remove OTP after successful registration

        if user:
            return JsonResponse(success_response(SuccessMessage.S00028.value, redirect="/sign-in/"), status=200)
        else:
            return JsonResponse(error_response(ErrorMessage.E00019.value, redirect="/sign-up/"), status=200)
    


class RequestOTPView(View):
    def get(self, request):
        email = request.GET.get("email")
        if not email:
            return JsonResponse(error_response(ErrorMessage.E00003.value))
        
        user = user_service.check_user_exist(email)
        if user:
            return JsonResponse(error_response(ErrorMessage.E00004.value))

        otp = random.randint(100000, 999999)
        OTP_STORAGE[email] = {"otp": otp, "verified": False, "timestamp": time.time()}

        print(f"Your {email} OTP is: {otp}")

        send_mail(
            subject="Your OTP Code",
            message=f"Your OTP is: {otp}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        msg = f"An OTP has been sent to {email}. Please check your email." # custom OTP Success Message
        
        return JsonResponse(success_response(msg), status=200)


@method_decorator(csrf_exempt, name='dispatch')
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

@method_decorator(csrf_exempt, name='dispatch')
class UserSigninView(View):
    def get(self, request):
        return render(request, "enduser/home/signin.html")

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        print("email:", email, "password:", password)

        try:
            user = user_service.check_user_exist(email)
            if check_password(password, user.password):  # Check hashed password
                login(request, user)  # Log in user
                request.session["email"] = user.email  # Store email in session
                return JsonResponse(success_response(SuccessMessage.S00001.value, redirect="/"), status=200)
            else:
                return JsonResponse(error_response(ErrorMessage.E00009.value))
        except:
            return JsonResponse(error_response(ErrorMessage.E00010.value))



class UserLogoutView(View):
    def get(self, request):
        logout(request)
        request.session.flush()  # Destroy session
        messages.success(request, SuccessMessage.S00014.value)
        return redirect("/sign-in/")
    

class CheckLoginStatus(View):
    """Handles checking login status for authenticated users."""
    def get(self, request):
        if request.user.is_authenticated:
            return JsonResponse(user_service.get_user_profile(request.user.id))
        return JsonResponse({"logged_in": False, "profile_photo_url": None})



OTP_STORAGE = {}
@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetView(View):
    def get(self, request):
        return render(request, 'enduser/home/password_reset.html')

    def post(self, request):
        try:
            # Parse JSON body
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")
            confirm_password = data.get("confirm_password")

            # Validation checks
            if email not in OTP_STORAGE or not OTP_STORAGE[email]["verified"]:
                return JsonResponse(error_response(ErrorMessage.E00028.value))

            if password != confirm_password:
                return JsonResponse(error_response(ErrorMessage.E00007.value))

            # Save the new password
            user = User.objects.get(email=email)
            user.password = make_password(password)
            user.save()

            # Clear OTP after password reset
            del OTP_STORAGE[email]

            return JsonResponse(success_response(SuccessMessage.S00027.value, redirect="/sign-in/"), status=200)

        except User.DoesNotExist:
            return JsonResponse(error_response(ErrorMessage.E00010.value))
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)


class ResetPasswordRequestOTPView(View):
    def get(self, request):
        email = request.GET.get("email")

        if not email:
            return JsonResponse(error_response(ErrorMessage.E00003.value))

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse(error_response(ErrorMessage.E00010.value))

        otp = random.randint(100000, 999999)
        OTP_STORAGE[email] = {"otp": otp, "verified": False, "timestamp": time.time()}

        print(f"Your OTP for {email} is: {otp}")  # For debugging, remove in production

        send_mail(
            subject="Your OTP Code",
            message=f"Your OTP is: {otp}",
            from_email=settings.EMAIL_HOST_USER,  # Use Django settings            
            recipient_list=[email],
            fail_silently=False,
        )

        msg = f"An OTP has been sent to {email}. Please check your email." # custom OTP Success Message
        
        return JsonResponse(success_response(msg), status=200)

@method_decorator(csrf_exempt, name='dispatch')
class ResetOtpVerificationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data.get("email")
        otp = data.get("otp")

        # Validate email and OTP
        if not email or not otp:
            return JsonResponse(error_response(ErrorMessage.E00029.value))

        # Check OTP in cache
        stored_otp = OTP_STORAGE.get(email, {}).get("otp")

        if not stored_otp:
            return JsonResponse(error_response(ErrorMessage.E00005.value))

        if str(stored_otp) != str(otp):
            return JsonResponse(error_response(ErrorMessage.E00006.value))

        # Mark OTP as verified
        OTP_STORAGE[email]["verified"] = True

        return JsonResponse(success_response(SuccessMessage.S00026.value))


OTP_STORAGE = {}
@auth_required(login_url='/login/admin/')
@role_required(Role.ADMIN.value, page_type='admin')
@method_decorator(csrf_exempt, name='dispatch')
class AdminPasswordUpdateView(View):
    def get(self, request):
        return render(request, 'adminuser/login/forgot_password.html')

    def post(self, request):
        email = request.POST.get("email")
        if request.user.email != email:
            return messages.error(request, ErrorMessage.E00030.value)

        try:
            password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            # Validation checks
            if email not in OTP_STORAGE or not OTP_STORAGE[email]["verified"]:
                return messages.error(request, ErrorMessage.E00028.value)

            if password != confirm_password:
                return messages.error(request, ErrorMessage.E00007.value)

            # Save the new password
            request.user.set_password(password)
            request.user.save()

            # Clear OTP after password reset
            del OTP_STORAGE[email]

            # Update session authentication hash to keep the user logged in
            update_session_auth_hash(request, request.user)
            messages.success(request, SuccessMessage.S00027.value)
            return redirect("/admin/profile/")

        except Exception as e:
            return messages.error(request, str(e))

