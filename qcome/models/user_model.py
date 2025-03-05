from django.db import models
from django.contrib.auth.models import AbstractUser
from ..constants import Gender, Role

class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    dob = models.DateField(null=False,blank=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    gender = models.IntegerField(
        choices=[(gender.value, gender.name) for gender in Gender],
        blank=True, null=True
    )
    roles = models.IntegerField(
        choices=[(r.value, r.name) for r in Role],
        blank=True,null=True
    )


    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_created=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"
