from fcm_django.models import FCMDevice
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import signals
from django.dispatch import receiver
from event.models import Notification, GroupMessage, Group, Event, Message, GroupInvitation
from event.notifications import create_notification
from django.contrib.auth.models import User


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


@receiver(signals.post_save, sender=GroupMessage)
def create_notification_group_message(sender, created, instance, **kwargs):
    if created:
        notification_type = 'group_message'
        gp_obj = Group.objects.get(id=instance.receiver_id)
        message = instance.msg
        get_member = gp_obj.member.all()

        # iterating through each member of a group
        for member in get_member:
            # sending push notification to all the members of a group
            try:
                device = FCMDevice.objects.get(user=member.id)
                device.send_message(title=gp_obj.name, body=message)
            except Exception as e:
                print(e)
                pass

        get_user_event = Event.objects.get(id=gp_obj.event_id)
        sender = instance.sender

        # creating notification
        # kwargs = {'user': sender, 'notification_type': notification_type, 'message': message, 'event': get_user_event,
        #           'group': gp_obj}
        # try:
        #     create_notification(**kwargs)
        # except Exception as e:
        #     print(e)


@receiver(signals.post_save, sender=Notification)
def send_push_notification(sender, created, instance, **kwargs):
    if created:
        # get current notification instance
        get_user = instance.user
        get_title = instance.notification_type
        if get_title == 'group_message' or get_title == 'group_invitation':
            pass
        else:
            get_message = instance.message
            try:
                device = FCMDevice.objects.get(user=get_user)
                device.send_message(title=get_title, body=get_message)
            except Exception as e:
                print(e)

    if not created:
        # get current notification instance
        get_user = instance.user
        get_title = instance.notification_type
        if get_title == 'group_message' or get_title == 'group_invitation':
            pass
        else:
            get_message = instance.message
            try:
                device = FCMDevice.objects.get(user=get_user)
                device.send_message(title=get_title, body=get_message)
            except Exception as e:
                print(e)


# @receiver(signals.post_save, sender=Message)
# def create_notification_dm_message(sender, created, instance, **kwargs):
#     if created:
#         notification_type = 'message'
#         user = instance.receiver
#         message = instance.msg
#         kwargs = {'user': user, 'notification_type': notification_type, 'message': message,
#                   'event': None, 'group': ''}
#         try:
#             create_notification(**kwargs)
#         except Exception as e:
#             print(e)


@receiver(signals.post_save, sender=Message)
def send_push_notification_for_dm_message(sender, created, instance, **kwargs):
    if created:
        # get current notification instance
        get_user = instance.receiver
        get_title = 'New Message'
        get_message = instance.msg
        try:
            device = FCMDevice.objects.get(user=get_user)
            device.send_message(title=get_title, body=get_message)
        except Exception as e:
            print(e)


@receiver(signals.post_save, sender=GroupInvitation)
def send_push_notification(sender, created, instance, **kwargs):
    if created:
        # send push notification when user invited other users to join the group
        invited_by = instance.invited_by
        invited_to = instance.invited_to
        invited_to_user = User.objects.filter(email=invited_to)
        if invited_to_user:
            invited_user = User.objects.get(email=invited_to)
            group = instance.group
            get_title = 'Group Invitation'
            get_message = f' {invited_by.first_name} has invited you to join an event group' f' {group.name}'
            try:
                device = FCMDevice.objects.get(user=invited_user)
                device.send_message(title=get_title, body=get_message)
            except Exception as e:
                print(e)

    if not created:
        # send push notification when user accepted the invitation
        invited_by = instance.invited_by
        invited_to = instance.invited_to
        status = instance.status
        group = instance.group
        get_title = 'Group Invitation'
        get_message = f' {invited_to} has {status} your invitation to join the group' f' {group.name}'
        try:
            device = FCMDevice.objects.get(user=invited_by)
            device.send_message(title=get_title, body=get_message)
        except Exception as e:
            print(e)
