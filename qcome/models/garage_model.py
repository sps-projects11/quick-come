from django.db import models
from ..constants import Vehicle_Type


class Garage(models.Model):
    garage_name = models.CharField(max_length=50)
    garage_owner = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    vehicle_type = models.IntegerField(
        choices=[(v_type.value, v_type.name) for v_type in Vehicle_Type],
        blank=False, null=False
    )
    garage_ac = models.CharField(max_length=50, null=False, blank=False)
    
    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_created=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, null=False, blank=True, related_name='fk_user_garage_create_users_id')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, related_name='fk_user_garage_update_users_id')


    REQUIRED_FIELDS = ['garage_name', 'garage_owner', 'phone', 'address']


    class Meta:
        db_table = 'garages'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"