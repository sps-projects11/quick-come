from django.db import models


class Worker(models.Model):
    worker = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_user_worker_users_id')
    garage = models.ForeignKey('Garage', on_delete=models.CASCADE, related_name='fk_garage_worker_garages_id')
    experience = models.CharField(max_length=15,null=True,blank=True)  # Years of Experience
    expertise = models.TextField(max_length=100, blank=False, null=False)  # Skills Description
    

    is_verified = models.BooleanField(default=False, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_created=True)


    class Meta:
        db_table = 'workers'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"

