from django.db import models
from django.contrib.auth.models import AbstractUser
from ..constants import Gender, Role

class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    dob = models.DateField(null=False, blank=False)
    profile_photo_url = models.URLField(max_length=200, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    gender = models.IntegerField(
        choices=[(gender.value, gender.name) for gender in Gender],
        blank=True, null=True
    )
    roles = models.IntegerField(
        choices=[(r.value, r.name) for r in Role],
        db_default=Role.END_USER.value,
        blank=True, null=True
    )

    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=False)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)


    # fields required for abstract user
    groups = None
    user_permissions = None
    username = models.CharField(max_length=128, blank=True, null=True)    
    is_staff = models.BooleanField(db_default=False, blank=True)  # To allow admin access
    is_superuser = models.BooleanField(db_default=False, blank=True)  # Superuser status
    
    # Use email as the username field.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"
