import firebase_admin
from firebase_admin import credentials
from quickcome import settings
import os
import json
from django.http import HttpResponse, JsonResponse
from firebase_admin import messaging
from qcome.services import user_service,user_notification_service
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


FIREBASE_CREDENTIALS_PATH = os.path.join(settings.BASE_DIR, 'static/js/serviceAccountKey.json')
if not firebase_admin._apps:
    cred = credentials.Certificate("static/js/serviceAccountkey (2).json")
    firebase_admin.initialize_app(cred)


def FirebaseMessagingSwFile(request):

    file_path = os.path.join(settings.BASE_DIR, 'static/js/firebase-messaging-sw.js')
    try:
        with open(file_path, 'r') as f:
            file_content = f.read()
        return HttpResponse(file_content, content_type='application/javascript')
    except FileNotFoundError:
        return HttpResponse("File not found", status=404)


def Firebasenotify(request):
    token = 'f3bmH8QRpmj3551wYsiG49:APA91bHPGxJEnfim2GHGT7tEeiqBxxPDo62Y1egqS9DPLOlSgCQZg7SY-hb0g854dkg5TI_vPmiHQT9-JrwPfUyhk83Uhv_B3Zesto1QIBmi_85UZmzgJdE'
    message = messaging.Message(
        notification=messaging.Notification(
            title='New Notification',
            body='Rima, you have a new notification',


        ),
        token=token 
    )
    print( message.notification.title,  message.notification.body)

    try:
        # Send the message
        response = messaging.send(message)
        print('Successfully sent message:', response)

        return JsonResponse({'status': 'success', 'message': 'Notification sent successfully.'})

    except Exception as e:
        print('Error sending message:', e)
        return JsonResponse({'status': 'error', 'message': str(e)})




@csrf_exempt
def save_fcm_token(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = request.user.id
            fcm_token = data.get("fcm_token")

            if not user_id or not fcm_token:
                return JsonResponse({"status": "error", "message": "Invalid data"}, status=400)

            user_service.updateFCMToken(user_id,fcm_token)

            return JsonResponse({"status": "success", "message": "FCM Token saved successfully"})
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=405)







# @csrf_exempt
# def send_notification(request):
#     if request.method == "POST":
#         try:
#             # Get data from the request (You can also use data from request.POST if not using JSON)
#             data = json.loads(request.body)

#             user_id = data.get("user_id")
#             title = data.get("title")
#             body = data.get("body")

#             # Fetch token dynamically
#             token =user_service.getFCMtoken(user_id) 

#             if not token:
#                 return JsonResponse({"success": False, "error": "FCM token not found"})

#             # Create message
#             message = messaging.Message(
#                 notification=messaging.Notification(title=title, body=body),
#                 token=token
#             )

#             # Send message
#             try:
#                 response = messaging.send(message)
#                  #For add Notification table
#                 following_id=user_id
#                 current_user_id=request.user.id
#                 user_notification_service.createNotification(body,current_user_id,following_id)
#                 return JsonResponse({"success": True, "message_id": response})
#             except Exception as e:
#                 return JsonResponse({"success": False, "error": str(e)})

#         except Exception as e:
#             return JsonResponse({"success": False, "error": "Invalid data"})

#     return JsonResponse({"success": False, "error": "Invalid request method"})