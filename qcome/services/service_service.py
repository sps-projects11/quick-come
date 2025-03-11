from qcome.models import User
from django.utils.timezone import now



def count_notification(user_id):
    return Notification.objects.filter(receiver_id=user_id)


def count_unread_notifications(user_id):
    return Notification.objects.filter(receiver_id=user_id, is_read=False).count()





def time_ago(time):
    diff = now() - time
    seconds = diff.total_seconds()

    if seconds < 60:
        return "just now"

    minutes = seconds // 60
    if minutes < 60:
        return f"{int(minutes)}m"

    hours = minutes // 60
    if hours < 24:
        return f"{int(hours)}h"

    days = hours // 24
    if days < 7:
        return f"{int(days)}d"


    return time.strftime('%b %d, %Y')

def createNotification(msgBody,user_id,receiver_id):
    instance_receiver_id=User.objects.get(id=receiver_id)
    instance_user_id=User.objects.get(id=user_id)
    Notification.objects.create(text=msgBody,created_by=instance_user_id,receiver_id=instance_receiver_id)