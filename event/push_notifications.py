from fcm_django.models import FCMDevice
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import signals
from django.dispatch import receiver
from event.models import Notification


class SendPushNotification(APIView):
    def get(self, request):
        try:
            get_user = self.request.user.id
        except:
            return Response({'error': 'User is not defined'})
        if get_user:
            device = FCMDevice.objects.get(user_id=get_user)
            try:
                device.send_message(title=request.data.get('title', ''), body=request.data.get('message', ''))
                return Response({'success', 'Notification has been sent'})
            except:
                return Response({'error': 'User Firebase Token is not registered yet'})


@receiver(signals.post_save, sender=Notification)
def send_push_notification(sender, created, instance, **kwargs):
    if created:
        # get current notification instance
        get_user = instance.user
        get_title = instance.notification_type
        get_message = instance.message
        try:
            device = FCMDevice.objects.get(user=get_user)
            device.send_message(title=get_title, body=get_message)
        except Exception as e:
            print(e)
