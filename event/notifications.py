from event.models import Notification


def create_notification(**kwargs):
    if kwargs['group'] == '':
        group = None
    else:
        group = kwargs['group']
    Notification.objects.create(
            user=kwargs['user'],
            notification_type=kwargs['notification_type'],
            message=kwargs['message'],
            event=kwargs['event'],
            group=group
        )
