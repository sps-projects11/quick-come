from qcome.models import User, Worker, Garage
from qcome.constants.default_values import Role
from django.db.models import Count


def get_user(user_id):
    return User.objects.get(id=user_id, is_active=True)


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
    active_users = User.objects.filter(is_active=True, roles=Role.END_USER.value)
    
    # Get IDs of active garage owners and workers
    garage_owner_ids = Garage.objects.filter(is_active=True).values_list('garage_owner', flat=True)
    worker_user_ids = Worker.objects.filter(is_active=True).values_list('worker', flat=True)
    
    # Exclude users who are garage owners or workers
    return active_users.exclude(id__in=garage_owner_ids).exclude(id__in=worker_user_ids)


def get_all_admins():
    return User.objects.filter(roles=Role.ADMIN.value, is_active=True)


def check_user_type(user_id):    
    if User.objects.filter(id=user_id, roles=Role.ADMIN.value, is_active=True).exists():
        return 'admin'
    elif Garage.objects.filter(garage_owner=user_id, is_active=True).exists():
        return 'garage'
    elif Worker.objects.filter(worker=user_id, is_active=True).exists():
        return 'worker'
    elif User.objects.filter(id=user_id, is_active=True, roles=Role.END_USER.value).exists():
        return 'end_user'
    return None


def get_monthly_user_data():
    """
    Returns a nested dictionary with month names as keys and values as dictionaries
    mapping user types (admin, garage, worker, end_user) to counts.
    For example:
      {
         'January': {'admin': 3, 'garage': 2, 'worker': 1, 'end_user': 5},
         'February': {'admin': 0, 'garage': 1, 'worker': 4, 'end_user': 2},
         ...
         'December': {'admin': 2, 'garage': 0, 'worker': 1, 'end_user': 3}
      }
    """
    # Map month numbers to month names
    month_mapping = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }
    
    # Fetch all users with the extracted month from created_at.
    # Using extra() here to extract month; depending on your DB backend you might also use ExtractMonth.
    users_qs = User.objects.all().extra(select={'month': 'EXTRACT(month FROM created_at)'}).values('id', 'month')
    
    # Initialize result dictionary for each month name with each user type set to 0.
    result = {month_name: {'admin': 0, 'garage': 0, 'worker': 0, 'end_user': 0} 
              for month_name in month_mapping.values()}
    
    for user in users_qs:
        user_id = user['id']
        try:
            month_number = int(user['month'])
        except (ValueError, TypeError):
            continue  # Skip if month cannot be determined
        
        month_name = month_mapping.get(month_number, None)
        if not month_name:
            continue  # Skip if no mapping is found

        # Determine the user type using your custom logic
        user_type = check_user_type(user_id)
        if user_type in result[month_name]:
            result[month_name][user_type] += 1
        else:
            # Optional: handle unexpected user types if needed
            pass

    return result


