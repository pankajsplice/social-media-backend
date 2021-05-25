from event.models import Notification


def create_notification(**kwargs):
    Notification.objects.create(
            user=kwargs['user'],
            notification_type=kwargs['notification_type'],
            message=kwargs['message'],
            event=kwargs['event']
        )
