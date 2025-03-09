from qcome.models import User


def get_user(user_id):
    return User.objects.get(id=user_id)


def get_user_profile(user_id):
    """Fetch user profile details by user ID."""
    data = User.objects.filter(id=user_id, is_active=True).values('profile_photo_url').first()

    if data:  # Ensure data is not None
        return {
            "logged_in": True,
            "profile_photo_url": data["profile_photo_url"] or '/static/all-Pictures/apps/avatar.jpg'
        }
    
    return {"logged_in": False, "profile_photo_url": None}  # Handle case where user does not exist


def get_user_details(user_id):
    data=User.objects.filter(id=user_id,is_active=True).values('id','first_name','last_name','profile_photo_url').first()
    print(data)
    if data:
        return{
            'id':data['id'],
            'fullname':f"{data['first_name']} {data['last_name']}",
            'photo': data["profile_photo_url"] or '/static/all-Pictures/apps/avatar.jpg'
        }
