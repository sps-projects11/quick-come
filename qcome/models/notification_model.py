from django.db import models

class Notification(models.Model):
    text = models.CharField(max_length=50, blank=True,null=True)
    media_url = models.URLField(max_length=200, blank=True,null=True) 
    receiver_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_user_notification_users_id')
    is_read = models.BooleanField(db_default=False, blank=True)
    
    is_active = models.BooleanField(db_default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, related_name='fk_create_notification_users_id')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='fk_update_notification_users_id')
  
    class Meta:
        db_table = 'notifications'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"
    






