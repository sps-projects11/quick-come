from django.db import models
class GarageWala(models.Model):
    garage_name = models.CharField(max_length=50)
    garage_owner = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    car_type = models.CharField(max_length=50)
    

    
    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_created=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    REQUIRED_FIELDS = ['garage_name', 'garage_owner', 'phone']


    class Meta:
        db_table = 'garages'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"