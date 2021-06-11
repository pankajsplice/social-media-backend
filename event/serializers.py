from event.models import Event, Category, Venue, Comment, Subscription, Like,\
    Follow, Message, Group, EventSetting, Notification
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

    class Meta:
        model = Event
        fields = ('id', 'name', 'global_id', 'url', 'price_min', 'price_max', 'event_status', 'currency',
                  'image_json', 'event_image', 'category', 'category_name', 'venue', 'venue_detail', 'seatmap_url', 'timezone', 'time', 'date',
                  'user', 'source', 'description', 'like', 'comment', 'group', 'created_by', 'updated_by', 'status',
                  'date_created', 'date_updated')

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
        ven = Venue.objects.get(id=obj.venue.id)
        venue_detail = {'name': ven.name, 'city': ven.city, 'state': ven.state_name, 'longitude': ven.longitude,
                        'latitude': ven.latitude, 'url': ven.url, 'country': ven.country_name, 'address': ven.address}
        return venue_detail

    def get_category_name(self, obj):
        cat = Category.objects.get(id=obj.category.id)
        return cat.name


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
        else:
            return None

    def get_event_detail(self, obj):
        event = Event.objects.get(id=obj.event.id)
        event_detail = {'name': event.name,  'event_status': event.event_status, 'date': event.date,
                        'url': event.url, 'time': event.time, 'currency': event.currency, 'source': event.source}
        return event_detail


class LikeSerializer(CustomBaseSerializer):
    event_detail = serializers.SerializerMethodField()
    user_detail = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = ('id', 'status', 'count', 'event', 'event_detail', 'created_by', 'updated_by', 'user_detail',
                  'date_created', 'date_updated')

    def get_user_detail(self, obj):
        if obj.created_by:
            user = User.objects.get(id=obj.created_by.pk)
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
        else:
            return None

    def get_event_detail(self, obj):
        event = Event.objects.get(id=obj.event.id)
        event_detail = {'name': event.name, 'event_status': event.event_status, 'date': event.date,
                        'url': event.url, 'time': event.time, 'currency': event.currency, 'source': event.source}
        return event_detail


class SubscriptionSerializer(CustomBaseSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class FollowSerializer(CustomBaseSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class MessageSerializer(CustomBaseSerializer):
    class Meta:
        model = Message
        fields = '__all__'


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
        fields = ('id', 'name', 'description', 'limit', 'member', 'event', 'event_name', 'total_member', 'created_by',
                  'updated_by', 'date_created', 'date_updated')

    def get_total_member(self, obj):
        member = obj.member.all().count()
        return member

    def get_event_name(self, obj):
        event_name = ''
        if obj.event:
            event_name = obj.event.name
        return event_name


class EventSettingSerializer(CustomBaseSerializer):
    event_detail = serializers.SerializerMethodField()
    user_detail = serializers.SerializerMethodField()

    class Meta:
        model = EventSetting
        fields = ('id', 'status', 'going', 'event', 'event_detail', 'user', 'user_detail', 'date_created',
                  'date_updated', 'created_by', 'updated_by')

    def get_event_detail(self, obj):
        event = Event.objects.get(id=obj.event.id)
        event_detail = {'name': event.name,  'event_status': event.event_status, 'date': event.date,
                        'url': event.url, 'time': event.time, 'currency': event.currency, 'source': event.source}
        return event_detail

    def get_user_detail(self, obj):
        user = User.objects.get(id=obj.user.id)
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


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
