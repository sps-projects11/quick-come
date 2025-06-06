from ..models import User

def admin_profile_update(user, first_name, middle_name, last_name, email, phone, gender, dob, profile_photo):
    
    user.first_name = first_name
    user.middle_name = middle_name
    user.last_name = last_name
    user.email = email
    user.phone = phone
    user.gender = gender
    user.dob = dob
    user.profile_photo_url = profile_photo
    user.updated_by = user
    user.save()
    return user