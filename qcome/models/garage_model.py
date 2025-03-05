from django.db import models
class Garage(models.Model):
    garage_name = models.CharField(max_length=50)
    garage_owner = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    
    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_created=True)

    
    REQUIRED_FIELDS = ['garage_name', 'garage_owner', 'phone', 'address']


    class Meta:
        db_table = 'garages'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"