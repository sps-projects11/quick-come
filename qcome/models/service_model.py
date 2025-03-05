from django.db import models
from ..constants import Gender



class Sevice(models.Model):
    status = models.CharField(max_length=50)
    work_by = models.CharField(max_length=50)
    worker_conatct = models.CharField(max_length=10)
    worker_gender = models.IntegerField(
        choices = [(gender.value,gender.name) for gender in Gender],
        blank = True,null = True 
    )



    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_created=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    class Meta:
        db_table = 'services'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"

