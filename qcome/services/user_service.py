from qcome.models import User, Worker, Garage
from qcome.constants.default_values import Role

def get_user(user_id):
    return User.objects.get(id=user_id)


def get_all_user():
    # Get all active end users
    users = User.objects.filter(roles=Role.END_USER.value)
    
    # Get IDs of users associated with active garages
    garage_user_ids = Garage.objects.filter(is_active=True).values_list('garage_owner', flat=True)
    # Get IDs of users associated with active workers
    worker_user_ids = Worker.objects.filter(is_active=True).values_list('worker', flat=True)
    
    # Combine the IDs to exclude
    exclude_ids = set(garage_user_ids).union(set(worker_user_ids))
    
    # Exclude users whose IDs are in the exclude_ids set
    final_users = users.exclude(id__in=exclude_ids)
    
    return final_users




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


def get_all_garages():
    return Garage.objects.filter(is_active=True) 


def user_create(first_name, middle_name, last_name, dob, email, phone, gender, profile_photo_path, user_password):
    return User.objects.create(
       first_name = first_name, 
       middle_name = middle_name, 
       last_name = last_name,
       dob = dob,
       email = email, 
       phone = phone, 
       gender = gender,
       profile_photo_url = profile_photo_path,
       password = user_password
    )


def toggle_user_status(user_id):
    try:
        # Use the primary key field "id" to get the user.
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None

    # Toggle the user's is_active status.
    user.is_active = not user.is_active
    user.save()
    return user
   

def user_phone_create(user, worker_phone):
    user=User.objects.filter(id=user).first()
    user.phone = worker_phone
    user.save()


def user_profile_photo_create(user, worker_profile_photo_path):
    user.profile_photo_url = worker_profile_photo_path
    user.save()


def user_name_update(user, first_name, middle_name, last_name):
    user.first_name = first_name
    user.middle_name = middle_name
    user.last_name = last_name
    user.save()


def get_non_garage_and_non_worker_users():
    active_users = User.objects.filter(is_active=True)
    
    # Get IDs of active garage owners and workers
    garage_owner_ids = Garage.objects.filter(is_active=True).values_list('garage_owner', flat=True)
    worker_user_ids = Worker.objects.filter(is_active=True).values_list('worker', flat=True)
    
    # Exclude users who are garage owners or workers
    return active_users.exclude(id__in=garage_owner_ids).exclude(id__in=worker_user_ids)


def get_all_admins():
    return User.objects.filter(roles=Role.ADMIN.value, is_active=True)