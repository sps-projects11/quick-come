from qcome.models import User
from ..models import User

def get_user(user_id):
    return User.objects.get(id=user_id)


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

