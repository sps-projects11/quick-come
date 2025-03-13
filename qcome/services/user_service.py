from qcome.models import User
from ..models import User

def get_user(user_id):
    return User.objects.get(id=user_id)

def get_all_user():
    return User.objects.all()


def get_user_profile(user_id):
    """Fetch user profile details by user ID."""
    data = User.objects.filter(id=user_id, is_active=True).values('profile_photo_url').first()

    if data:  # Ensure data is not None
        return {
            "logged_in": True,
            "profile_photo_url": data["profile_photo_url"] or '/static/all-Pictures/admin-person.jpg'
        }
    
    return {"logged_in": False, "profile_photo_url": None}  # Handle case where user does not exist




def get_user_details(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None
    
    
def update_user_details(user, data):
    user.first_name = data.get('first_name')
    user.middle_name = data.get('middle_name')
    user.last_name = data.get('last_name')
    user.email = data.get('email')
    user.phone = data.get('phone')

    gender = data.get('gender')
    if gender == 'Male':
        user.gender = 1
    elif gender == 'Female':
        user.gender = 2
    elif gender == 'Other':
        user.gender = 3

    user.dob = data.get('dob')
    user.profile_photo_url = data.get('profile_photo_url', user.profile_photo_url)

    user.save()
    return user


    
def updateFCMToken(user_id,fcm_token):
    user = User.objects.get(id=user_id)
    user.fcm_token = fcm_token
    user.save()

def getFCMtoken(user_id):
    return User.objects.filter(id=user_id).values_list('fcm_token', flat=True).first()
