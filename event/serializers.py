from event.models import Event, Category, Venue, Comment, Subscription, Like,\
    Follow, Message, Group, EventSetting, Notification, GroupMessage, RecurringEvent, GroupInvitation, MessageSetting
from utils.custom_mixin import QuerySetFilterMixin, CustomBaseSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import UserProfile
from accounts.serializers import UserSerializer

User = get_user_model()


class EventSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()
    venue_detail = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    date = serializers.DateField(input_formats=['%d-%m-%Y', ])
    user_detail = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'name', 'global_id', 'url', 'price_min', 'price_max', 'event_status', 'currency',
                  'image_json', 'event_image', 'category', 'category_name', 'venue', 'venue_detail', 'seatmap_url', 'timezone', 'time', 'date',
                  'user', 'source', 'description', 'like', 'comment', 'group', 'created_by', 'updated_by', 'user_detail', 'status',
                  'date_created', 'date_updated', 'recurring')

    def get_like(self, obj):
        like = Like.objects.filter(event_id=obj.id).count()
        return like

    def get_comment(self, obj):
        comment = Comment.objects.filter(event_id=obj.id).count()
        return comment

    def get_group(self, obj):
        group = Group.objects.filter(event_id=obj.id).count()
        return group

    def get_venue_detail(self, obj):
        if obj.venue:
            ven = Venue.objects.get(id=obj.venue.id)
            venue_detail = {'name': ven.name, 'city': ven.city, 'state': ven.state_name, 'longitude': ven.longitude,
                            'latitude': ven.latitude, 'url': ven.url, 'country': ven.country_name,
                            'address': ven.address, 'postal_code': ven.postal_code}
            return venue_detail
        return None

    def get_category_name(self, obj):
        cat = Category.objects.get(id=obj.category.id)
        return cat.name

    def get_user_detail(self, obj):
        if obj.created_by:
            user = User.objects.get(id=obj.created_by.pk)
            try:
                user_profile = UserProfile.objects.get(user=user)
                if user_profile:
                    profile = user_profile.profile_pic
                    mobile = user_profile.mobile
                    if profile:
                        profile = profile.url
                    else:
                        profile = None
                else:
                    profile = None
                    mobile = None
                user_detail = {'name': f'{user.first_name} {user.last_name}', 'email': user.email, 'profile': profile,
                               'mobile': mobile}
                return user_detail
            except:
                user_detail = {'name': f'{user.first_name} {user.last_name}', 'email': user.email}
                return user_detail
        else:
            return None


class CategorySerializer(CustomBaseSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class VenueSerializer(CustomBaseSerializer):
    class Meta:
        model = Venue
        fields = '__all__'


class CommentSerializer(CustomBaseSerializer):
    user_detail = serializers.SerializerMethodField()
    event_detail = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'event', 'event_detail', 'msg', 'verified', 'created_by', 'updated_by', 'status', 'user_detail',
                  'date_created', 'date_updated')

    def get_user_detail(self, obj):
        if obj.created_by:
            user = User.objects.get(id=obj.created_by.pk)
            try:
                user_profile = UserProfile.objects.get(user=user)
                if user_profile:
                    profile = user_profile.profile_pic
                    mobile = user_profile.mobile
                    if profile:
                        profile = profile.url
                    else:
                        profile = None
                else:
                    profile = None
                    mobile = None
                user_detail = {'name': f'{user.first_name} {user.last_name}', 'email': user.email, 'profile': profile,
                               'mobile': mobile}
                return user_detail
            except:
                user_detail = {'name': f'{user.first_name} {user.last_name}', 'email': user.email}
                return user_detail
        else:
            return None

    def get_event_detail(self, obj):
        event = Event.objects.get(id=obj.event.id)
        if event.event_image:
            ev_img = event.event_image.url
        else:
            ev_img = None
        event_detail = {'name': event.name,  'event_status': event.event_status, 'date': event.date,
                        'url': event.url, 'time': event.time, 'currency': event.currency, 'source': event.source,
                        'event_image': ev_img, 'image_json': event.image_json}
        return event_detail


class LikeSerializer(CustomBaseSerializer):
    event_detail = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = ('id', 'status', 'count', 'event', 'event_detail', 'created_by', 'updated_by', 'like',
                  'date_created', 'date_updated')

    def get_like(self, obj):
        if obj.created_by:
            return True
        else:
            return False

    def get_event_detail(self, obj):
        event = Event.objects.get(id=obj.event.id)
        if event.event_image:
            ev_img = event.event_image.url
        else:
            ev_img = None
        event_detail = {'name': event.name, 'event_status': event.event_status, 'date': event.date,
                        'url': event.url, 'time': event.time, 'currency': event.currency, 'source': event.source,
                        'event_image': ev_img, 'image_json': event.image_json}
        return event_detail


class SubscriptionSerializer(CustomBaseSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class FollowSerializer(CustomBaseSerializer):
    interested = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'event',  'user', 'interested')

    def get_interested(self, obj):
        if obj:
            return True


class MessageSerializer(CustomBaseSerializer):

    sender_detail = serializers.SerializerMethodField()
    receiver_detail = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ('id', 'sender', 'sender_detail', 'receiver', 'receiver_detail', 'msg', 'date_created', 'date_updated', 'status')

    def get_sender_detail(self, obj):
        if obj.sender:
            user = User.objects.get(id=obj.sender.id)
            try:
                user_profile = UserProfile.objects.get(user=user)
                if user_profile:
                    profile = user_profile.profile_pic
                    mobile = user_profile.mobile
                    if profile:
                        profile = profile.url
                    else:
                        profile = None
                else:
                    profile = None
                    mobile = None
                user_detail = {'name': f'{user.first_name} {user.last_name}', 'email': user.email, 'profile': profile,
                               'mobile': mobile}
                return user_detail
            except:
                user_detail = {'name': f'{user.first_name} {user.last_name}', 'email': user.email}
                return user_detail
        else:
            return None

    def get_receiver_detail(self, obj):
        if obj.receiver:
            user = User.objects.get(id=obj.receiver.id)
            try:
                user_profile = UserProfile.objects.get(user=user)
                if user_profile:
                    profile = user_profile.profile_pic
                    mobile = user_profile.mobile
                    if profile:
                        profile = profile.url
                    else:
                        profile = None
                else:
                    profile = None
                    mobile = None
                user_detail = {'name': f'{user.first_name} {user.last_name}', 'email': user.email, 'profile': profile,
                               'mobile': mobile}
                return user_detail
            except:
                user_detail = {'name': f'{user.first_name} {user.last_name}', 'email': user.email}
                return user_detail
        else:
            return None


class PostGroupSerializer(CustomBaseSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class GetGroupSerializer(CustomBaseSerializer):
    member = UserSerializer(read_only=True, many=True)
    total_member = serializers.SerializerMethodField()
    event_name = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('id', 'name', 'icon', 'description', 'limit', 'member', 'event', 'event_name', 'total_member', 'created_by',
                  'updated_by', 'date_created', 'date_updated')

    def get_total_member(self, obj):
        member = obj.member.all().count()
        return member

    def get_event_name(self, obj):
        event_name = ''
        if obj.event:
            event_name = obj.event.name
        return event_name


class EventSettingSerializer(serializers.ModelSerializer):
    recurring_event = serializers.PrimaryKeyRelatedField(html_cutoff=10, queryset=RecurringEvent.objects.all(),
                                                         allow_null=True)
    event_detail = serializers.SerializerMethodField()
    user_detail = serializers.SerializerMethodField()
    recurring_event_detail = serializers.SerializerMethodField()

    class Meta:
        model = EventSetting
        fields = ('id', 'status', 'going', 'event', 'event_detail', 'user', 'user_detail', 'recurring_event',
                  'recurring_event_detail', 'date_created', 'date_updated', 'created_by', 'updated_by')

    def get_event_detail(self, obj):
        event = Event.objects.get(id=obj.event.id)
        if event.event_image:
            ev_img = event.event_image.url
        else:
            ev_img = None
        event_detail = {'name': event.name,  'event_status': event.event_status, 'date': event.date,
                        'url': event.url, 'time': event.time, 'currency': event.currency, 'source': event.source,
                        'event_image': ev_img, 'image_json': event.image_json}
        return event_detail

    def get_user_detail(self, obj):
        if obj.user:
            user = User.objects.get(id=obj.user.id)
            try:
                user_profile = UserProfile.objects.get(user=user)
                if user_profile:
                    profile = user_profile.profile_pic
                    mobile = user_profile.mobile
                    if profile:
                        profile = profile.url
                    else:
                        profile = None
                else:
                    profile = None
                    mobile = None
                user_detail = {'name': f'{user.first_name} {user.last_name}', 'email': user.email, 'profile': profile,
                               'mobile': mobile}
                return user_detail
            except:
                user_detail = {'name': f'{user.first_name} {user.last_name}', 'email': user.email}
                return user_detail
        else:
            return None

    def get_recurring_event_detail(self, obj):
        if obj.recurring_event:
            date = obj.recurring_event.date
            recurring_event_detail = {'event': obj.recurring_event.event_id, 'date': obj.recurring_event.date,
                                      'time': obj.recurring_event.time}
            return recurring_event_detail
        else:
            return None


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class GroupMessageSerializer(CustomBaseSerializer):
    user_detail = serializers.SerializerMethodField()
    group_detail = serializers.SerializerMethodField()

    class Meta:
        model = GroupMessage
        fields = ('id', 'sender', 'user_detail', 'receiver', 'group_detail', 'msg', 'timestamp', 'is_read')

    def get_group_detail(self, obj):
        try:
            name = obj.receiver.name
            icon = obj.receiver.icon
            if icon:
                icon = icon.url
            else:
                icon = None
            return {"id": obj.receiver.id, "name": name, "group_icon": icon}
        except:
            name = obj.receiver.name
            return {"id": obj.receiver.id, "name": name, "group_icon": None}

    def get_user_detail(self, obj):
        if obj.sender:
            user = User.objects.get(id=obj.sender.id)
            try:
                user_profile = UserProfile.objects.get(user=user)
                if user_profile:
                    profile = user_profile.profile_pic
                    mobile = user_profile.mobile
                    if profile:
                        profile = profile.url
                    else:
                        profile = None
                else:
                    profile = None
                    mobile = None
                user_detail = {'name': f'{user.first_name} {user.last_name}', 'email': user.email, 'profile': profile,
                               'mobile': mobile}
                return user_detail
            except:
                user_detail = {'name': f'{user.first_name} {user.last_name}', 'email': user.email}
                return user_detail
        else:
            return None


class RecurringEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringEvent
        fields = '__all__'


class GroupInvitationSerializer(serializers.ModelSerializer):
    group_detail = serializers.SerializerMethodField()
    invited_by_detail = serializers.SerializerMethodField()
    invited_to_detail = serializers.SerializerMethodField()

    class Meta:
        model = GroupInvitation
        fields = ('id', 'group', 'group_detail', 'invited_by', 'invited_by_detail', 'invited_to',
                  'invited_to_detail', 'status')

    def get_group_detail(self, obj):
        try:
            name = obj.receiver.name
            icon = obj.receiver.icon
            if icon:
                icon = icon.url
            else:
                icon = None
            return {"id": obj.receiver.id, "name": name, "group_icon": icon}
        except:
            name = obj.receiver.name
            return {"id": obj.receiver.id, "name": name, "group_icon": None}

    def get_invited_by_detail(self, obj):
        if obj.invited_by:
            user = User.objects.get(id=obj.invited_by.id)
            try:
                user_profile = UserProfile.objects.get(user=user)
                if user_profile:
                    profile = user_profile.profile_pic
                    mobile = user_profile.mobile
                    if profile:
                        profile = profile.url
                    else:
                        profile = None
                else:
                    profile = None
                    mobile = None
                user_detail = {'name': f'{user.first_name} {user.last_name}', 'email': user.email, 'profile': profile,
                               'mobile': mobile}
                return user_detail
            except:
                user_detail = {'name': f'{user.first_name} {user.last_name}', 'email': user.email}
                return user_detail
        else:
            return None

    def get_invited_to_detail(self, obj):
        if obj.invited_to:
            try:
                user = User.objects.get(email=obj.invited_to)
                try:
                    user_profile = UserProfile.objects.get(user=user)
                    if user_profile:
                        profile = user_profile.profile_pic
                        mobile = user_profile.mobile
                        if profile:
                            profile = profile.url
                        else:
                            profile = None
                    else:
                        profile = None
                        mobile = None
                    user_detail = {'name': f'{user.first_name} {user.last_name}', 'email': user.email, 'profile': profile,
                                   'mobile': mobile}
                    return user_detail
                except:
                    user_detail = {'name': f'{user.first_name} {user.last_name}', 'email': user.email}
                    return user_detail
            except:
                return None
        else:
            return None


class MessageSettingSerializer(serializers.ModelSerializer):
    sender_detail = serializers.SerializerMethodField()
    receiver_detail = serializers.SerializerMethodField()

    class Meta:
        model = MessageSetting
        fields = ('id', 'sender', 'sender_detail', 'receiver', 'receiver_detail', 'block', 'report', 'date_created')

    def get_sender_detail(self, obj):
        if obj.sender:
            user = User.objects.get(id=obj.sender.id)
            try:
                user_profile = UserProfile.objects.get(user=user)
                if user_profile:
                    profile = user_profile.profile_pic
                    mobile = user_profile.mobile
                    if profile:
                        profile = profile.url
                    else:
                        profile = None
                else:
                    profile = None
                    mobile = None
                user_detail = {'name': f'{user.first_name} {user.last_name}', 'email': user.email, 'profile': profile,
                               'mobile': mobile}
                return user_detail
            except:
                user_detail = {'name': f'{user.first_name} {user.last_name}', 'email': user.email}
                return user_detail
        else:
            return None

    def get_receiver_detail(self, obj):
        if obj.receiver:
            user = User.objects.get(id=obj.receiver.id)
            try:
                user_profile = UserProfile.objects.get(user=user)
                if user_profile:
                    profile = user_profile.profile_pic
                    mobile = user_profile.mobile
                    if profile:
                        profile = profile.url
                    else:
                        profile = None
                else:
                    profile = None
                    mobile = None
                user_detail = {'name': f'{user.first_name} {user.last_name}', 'email': user.email, 'profile': profile,
                               'mobile': mobile}
                return user_detail
            except:
                user_detail = {'name': f'{user.first_name} {user.last_name}', 'email': user.email}
                return user_detail
        else:
            return None