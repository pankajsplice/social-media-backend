from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django_filters import rest_framework as filters
from rest_framework import authentication, permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.custom_mixin import QuerySetFilterMixin
from event.models import Event, Category, Venue, Comment, Like, Subscription,\
    Follow, Message, Group, EventSetting, Notification, GroupMessage, RecurringEvent, GroupInvitation, MessageSetting
from event.serializers import EventSerializer, CategorySerializer, VenueSerializer, \
    CommentSerializer, LikeSerializer, SubscriptionSerializer, FollowSerializer, MessageSerializer, \
    PostGroupSerializer, GetGroupSerializer, EventSettingSerializer, NotificationSerializer, GroupMessageSerializer, \
    RecurringEventSerializer, GroupInvitationSerializer, MessageSettingSerializer, GetGroupMemberSerializer

from event.ticketmaster import GetEventList
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q
from accounts.models import UserProfile
from accounts.serializers import UserProfileSerializer, UserSerializer
from rest_framework.generics import ListAPIView, ListCreateAPIView
from event.notifications import create_notification
from django.core.mail import send_mail, EmailMultiAlternatives
from local_mingle_backend.settings import DEFAULT_FROM_EMAIL, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from event.location_filter import get_location
from rest_framework.pagination import PageNumberPagination
from datetime import datetime
from rest_framework import status

User = get_user_model()


# to create events
class EventViewSet(QuerySetFilterMixin, viewsets.ModelViewSet):
    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = {'status': ['exact'],
                        'venue__name': ['iexact', 'istartswith'],
                        'category__name': ['iexact', 'istartswith'],
                        'name': ['iexact', 'istartswith'],
                        'event_status': ['iexact', 'istartswith'],
                        'date': ['gte', 'lte', 'exact'],
                        'category__parent_id': ['exact'],
                        'category_id': ['exact'],
                        'source': ['iexact'],
                        'id': ['exact'],
                        'created_by__id': ['exact'],
                        # 'venue__latitude': ['exact', 'startswith'],
                        # 'venue__longitude': ['exact', 'startswith'],
                        }

    def get_queryset(self):
        queryset = Event.objects.filter(date__gte=datetime.today())
        venue_lat = self.request.query_params.get('venue__latitude', None)
        location = self.request.query_params.get('location', None)
        venue_long = self.request.query_params.get('venue__longitude', None)
        if venue_long and venue_lat:
            res = get_location(venue_lat, venue_long)
            queryset = queryset.filter(venue__in=res)
        if location:
            queryset = queryset.filter(Q(venue__city__istartswith=location) | Q(venue__state_name__istartswith=location)
                                       | Q(venue__postal_code__istartswith=location)).order_by('-id')
        return queryset


# to create events' category
class CategoryViewSet(viewsets.ModelViewSet):
    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filterset_fields = {
        'name': ['iexact', 'istartswith'],
        'parent': ['exact', 'isnull'],
        'level': ['exact']
    }


# to create events' Venue details
class VenueViewSet(QuerySetFilterMixin, viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = VenueSerializer
    queryset = Venue.objects.all()


# fetch events details from ticketmaster source
class FetchEventTicketMasterApiView(APIView):

    def get(self, *args):
        category = self.request.query_params['category']
        event = GetEventList(category)
        result = event.fetch()
        pg_limit = 0
        for page in result:
            pg_limit = pg_limit + 1
            if pg_limit == 50:
                return Response({'status': 'Max paging depth exceeded for category '+self.request.query_params['category']})
            if page.size == 0:
                return Response({'status': 'Not Found any data from the data source related to '+self.request.query_params['category']})
            for event in page:
                if event.status == 'cancelled':
                    pass
                else:
                    # creating venue
                    ven_id = None
                    venue_instance = None
                    if event.venues:
                        global_venue_json = event.venues[0].json
                        # check if venue already exists
                        venue_availability = Venue.objects.filter(global_id=global_venue_json['id']).values('id')
                        if venue_availability.exists():
                            for venue in venue_availability:
                                ven_id = venue['id']
                        else:
                            global_id = city = country_code = country_name = ''
                            try:
                                state = global_venue_json.get('state', '')
                                if state == '':
                                    state_code = ''
                                    state_name = ''
                                else:
                                    state_code = global_venue_json['state']['stateCode']
                                    state_name = global_venue_json['state']['name']

                                address = global_venue_json.get('address', '')
                                if address == '':
                                    address = address
                                else:
                                    address = global_venue_json['address']['line1']

                                location = global_venue_json.get('location', '')
                                if location == '':
                                    longitude = ''
                                    latitude = ''
                                else:
                                    longitude = global_venue_json['location']['longitude']
                                    latitude = global_venue_json['location']['latitude']

                                country = global_venue_json.get('country', '')
                                if country == '':
                                    country_code = ''
                                    country_name = ''
                                else:
                                    country_code = global_venue_json['country']['countryCode']
                                    country_name = global_venue_json['country']['name']

                                city = global_venue_json.get('city', '')
                                if city == '':
                                    city = city
                                else:
                                    city = global_venue_json['city']['name']

                                postal_code = global_venue_json.get('postalCode', '')
                                url = global_venue_json.get('url', '')
                                name = global_venue_json.get('name', '')
                                global_id = global_venue_json.get('id', '')
                            except:
                                state_code = state_name = postal_code = address = longitude = latitude = url = name = ''

                            venue_instance = Venue(name=name, global_id=global_id,
                                                   city=city, address=address,
                                                   state_code=state_code,
                                                   state_name=state_name,
                                                   postal_code=postal_code,
                                                   country_code=country_code,
                                                   country_name=country_name,
                                                   latitude=latitude,
                                                   longitude=longitude,
                                                   url=url)
                            venue_instance.save()
                            print(venue_instance.pk)
                        # creating category
                        genre_id, genre_name, genre = None, None, False
                        # check if sub-category is available in data source
                        try:
                            genre_name = event.classifications[0].json['genre']['name']
                            genre = True
                        except:
                            genre = False
                        category_name = event.classifications[0].json['segment']['name']
                        if genre:
                            genre_name = event.classifications[0].json['genre']['name']
                        category_availability = Category.objects.filter(name=category_name).values('name', 'id')
                        category_instance = None
                        if category_availability.exists():
                            for cat in category_availability:
                                if genre:
                                    genre_availability = Category.objects.filter(name=genre_name).values('name', 'id')
                                    if genre_availability.exists():
                                        for gen in genre_availability:
                                            genre_id = gen['id']
                                    else:
                                        parent_id = cat['id']
                                        category_instance = Category(name=genre_name, parent_id=parent_id)
                                        category_instance.save()
                                else:
                                    genre_id = cat['id']

                        else:
                            category_instance = Category(name=category_name)
                            category_instance.save()
                            category_availability = Category.objects.filter(name=category_name).values('name', 'id')
                            if category_availability.exists():
                                for cat in category_availability:
                                    if genre:
                                        genre_availability = Category.objects.filter(name=genre_name).values('name', 'id')
                                        if genre_availability.exists():
                                            for gen in genre_availability:
                                                genre_id = gen['id']
                                        else:
                                            parent_id = cat['id']
                                            category_instance = Category(name=genre_name, parent_id=parent_id)
                                            category_instance.save()
                                    else:
                                        genre_id = cat['id']
                            print(category_instance.pk)
                        # getting category and venue id
                        try:
                            category_id = category_instance.pk
                        except:
                            category_id = genre_id
                        try:
                            venue_id = venue_instance.pk
                        except:
                            venue_id = ven_id
                        price_min = price_max = currency = ''
                        if len(event.price_ranges) > 0:
                            price_min = event.json['priceRanges'][0]['min']
                            price_max = event.json['priceRanges'][0]['max']
                            currency = event.json['priceRanges'][0]['currency']

                        # creating event
                        global_event_json = event.json
                        # check if events already exists
                        event_availability = Event.objects.filter(global_id=global_event_json['id'])

                        # check for recurring events exists
                        event_recurring = Event.objects.filter(name=global_event_json['name'])
                        if event_availability.exists():
                            pass
                        elif event_recurring.exists():
                            if event_recurring.count() == 1:
                                event_obj = Event.objects.get(name=global_event_json['name'])
                                if event_obj.event_status == event.status and event_obj.venue.id == venue_id:
                                    event_recurring.update(recurring=True)
                                    if event_obj.recurring:
                                        recurring_event = RecurringEvent(event_id=event_obj.id, time=event.local_start_time,
                                                                         date=event.local_start_date,)
                                        recurring_event.save()
                                else:
                                    pass
                            else:
                                pass
                        else:
                            try:
                                timezone = event.json['dates']['timezone']
                            except:
                                timezone = ''
                            event_instance = Event(name=global_event_json['name'], global_id=global_event_json['id'],
                                                   url=global_event_json['url'], price_min=price_min, price_max=price_max,
                                                   event_status=event.status, currency=currency, image_json=global_event_json['images'],
                                                   category_id=category_id, venue_id=venue_id, seatmap_url='',
                                                   timezone=timezone, time=event.local_start_time,
                                                   date=event.local_start_date, description='', recurring=False)
                            event_instance.save()
                    else:
                        print(event)
                        pass
        return Response({'status': 'ok'})


# crud for comment
class CommentViewSet(QuerySetFilterMixin, viewsets.ModelViewSet):
    # pagination_class = None
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    filterset_fields = ['event__id', 'created_by__id']

    def get_queryset(self):
        # queryset = Comment.objects.filter(event__date__gte=datetime.today())
        queryset = super().get_queryset()

        # adding filter when user has enabled his profile_interest then only anyone can see his comment details

        comment_id = []
        event = []
        for q in queryset:
            if q.created_by:
                if q.created_by == self.request.user:
                    if q.id not in comment_id:
                        if q.event_id not in event:
                            event.append(q.event_id)
                            comment_id.append(q.id)
                else:
                    get_profile = UserProfile.objects.get(user=q.created_by)
                    if get_profile.profile_interest:
                        if q.id not in comment_id:
                            if q.event_id not in event:
                                event.append(q.event_id)
                                comment_id.append(q.id)

        new_queryset = queryset.filter(id__in=comment_id)

        event_filter = self.request.query_params.get('event__id', '')
        if event_filter != '':
            queryset = Comment.objects.filter(event__date__gte=datetime.today())
            # queryset = super().get_queryset()
            comment_id = []
            for q in queryset:
                if q.created_by:
                    if q.created_by == self.request.user:
                        if q.id not in comment_id:
                            comment_id.append(q.id)
                    else:
                        get_profile = UserProfile.objects.get(user=q.created_by)
                        if get_profile.profile_interest:
                            if q.id not in comment_id:
                                comment_id.append(q.id)

            new_queryset = queryset.filter(id__in=comment_id)

        return new_queryset


# crud for like
class LikeViewSet(QuerySetFilterMixin, viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    filterset_fields = ['event__id', 'created_by__id']

    def get_queryset(self):
        queryset = Follow.objects.filter(event__date__gte=datetime.today())
        return queryset


# crud for subscription
class SubscriptionViewSet(QuerySetFilterMixin, viewsets.ModelViewSet):
    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class FollowViewSet(QuerySetFilterMixin, viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    filterset_fields = ['event__id', 'user__id']

    def get_queryset(self):
        queryset = Follow.objects.filter(event__date__gte=datetime.today())
        return queryset


class MessageViewSet(QuerySetFilterMixin, viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MessageSerializer
    queryset = Message.objects.all()


class PostGroupViewSet(QuerySetFilterMixin, viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PostGroupSerializer
    queryset = Group.objects.all()


class GetGroupList(ListAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GetGroupSerializer
    queryset = Group.objects.all()
    filterset_fields = ['id', 'event__id']

    def get_queryset(self):
        if self.request.user:
            queryset = self.queryset.filter(Q(member=self.request.user, event__date__gte=datetime.today()) |
                                            Q(created_by=self.request.user, event__date__gte=datetime.today())).distinct()
            # queryset = self.queryset.filter(Q(member=self.request.user) |
            #                                 Q(created_by=self.request.user)).distinct()
            return queryset
        else:
            return self.queryset

    def get_serializer_context(self):
        context = super(GetGroupList, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class EventSettingViewSet(QuerySetFilterMixin, viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EventSettingSerializer
    queryset = EventSetting.objects.all()
    filterset_fields = {'event__name': ['iexact', 'istartswith'],
                        'event': ['exact'],
                        'going': ['exact'],
                        'user__id': ['exact']}

    def get_queryset(self):
        queryset = EventSetting.objects.filter(event__date__gte=datetime.today())
        # queryset = super().get_queryset()
        event_setting_id = []
        # adding filter when user has enabled his profile_interest then only anyone can see his going details
        for q in queryset:
            if q.user:
                if q.user == self.request.user:
                    if q.id not in event_setting_id:
                        event_setting_id.append(q.id)
                else:
                    get_profile = UserProfile.objects.get(user=q.user)
                    if get_profile.profile_interest:
                        if q.id not in event_setting_id:
                            event_setting_id.append(q.id)

        new_queryset = queryset.filter(id__in=event_setting_id)
        return new_queryset


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notification.objects.all().order_by('-id')
    serializer_class = NotificationSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_superuser:
            queryset = super().get_queryset().filter(user=self.request.user)

        return queryset


class MessageUser(APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request, id):
        messages_query = Message.objects.filter(Q(sender=id) | Q(receiver=id)).order_by('-id')
        print('messages_query', messages_query)
        message_user = list(set([]))
        for i in messages_query:
            if (int(i.sender.id) != int(id)) or (int(i.receiver.id) != int(id)):
                message_user.append(i.sender.id)
                message_user.append(i.receiver.id)
        recent_message_user = User.objects.filter(id__in=message_user)
        data = []
        for i in recent_message_user:
            serializer = UserSerializer(i)
            check_profile = UserProfile.objects.filter(user=i.id)
            user = serializer.data
            if check_profile:
                profile = UserProfile.objects.get(user=i.id)
                serializer_profile = UserProfileSerializer(profile)
                print(profile.profile_pic)
                user['profile'] = serializer_profile.data
            else:
                user['profile'] = None
            messages = Message.objects.filter(Q(sender__in=[i.id, request.user.id]), Q(receiver__in=[request.user.id, i.id])).order_by(
                '-id').first()
            serializer_message = MessageSerializer(messages)
            if len(serializer_message.data['msg']) >= 1:
                user['msg'] = serializer_message.data
            data.append(user)
        return Response(data)


class MessageView(APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request, user, friend):
        msg = Message.objects.filter(Q(sender=user, receiver=friend) | Q(sender=friend, receiver=user)).order_by('id', 'date_created')
        messages = []
        for m in msg:
            serializer = MessageSerializer(m)
            messages.append(serializer.data)
        return Response(messages)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class GroupInvitationApi(APIView):

    def post(self, request, format=None):
        get_email = request.data.get('email', '')
        mobile = request.data.get('mobile', '')
        group = request.data.get('group', '')
        if group != '':
            gp = Group.objects.get(id=group)
            try:
                event = Event.objects.get(id=gp.event_id)
            except:
                event = ''
            if get_email != '':
                try:
                    user = User.objects.get(email=get_email)
                    group_invitation_instance = GroupInvitation.objects.filter(group_id=group,
                                                                               invited_to=get_email)
                    if group_invitation_instance:
                        return Response({'error': 'User is already invited', 'status': status.HTTP_404_NOT_FOUND})
                    else:
                        email_message = 'You are invited to join the group' f' {gp.name} ' 'for the event' f' {event.name}'

                        subject = 'LocalMingle Group Invitation'
                        text_content = ''
                        html_content = render_to_string('mail/group_invitation.html', {
                            "message": email_message,
                            "user": f"{user.first_name} {user.last_name}",
                            "app_install": False,
                        })
                        msg = EmailMultiAlternatives(subject, text_content, DEFAULT_FROM_EMAIL, [get_email])
                        msg.attach_alternative(html_content, "text/html")

                        # creating notification start
                        notification_type = 'group_invitation'
                        get_user_event = Event.objects.get(id=gp.event_id)
                        message = 'You have got an invitation to join the group' f' {gp.name}'
                        kwargs = {'user': user, 'notification_type': notification_type, 'message': message,
                                  'event': get_user_event, 'group': gp}
                        create_notification(**kwargs)
                        # creating notification end
                        try:
                            msg.send()
                            return Response({'success': 'Group Invitation sent'})

                        except Exception as e:
                            return Response({'error': 'Group Invitation can not sent'})

                except Exception as e:
                    print(e)
                    group_invitation_instance = GroupInvitation.objects.filter(group_id=group,
                                                                               invited_to=get_email)
                    if group_invitation_instance:
                        return Response({'error': 'User is already invited', 'status': status.HTTP_404_NOT_FOUND})
                    else:
                        subject = 'LocalMingle Group Invitation'
                        text_content = ''
                        android_link = "https://play.google.com/store/apps/details?id=com.local_mingle"
                        ios_link = ""
                        email_message = 'You are invited to join Local-mingle application. Click on below buttons to ' \
                                        'install and register it for free.'
                        html_content = render_to_string('mail/group_invitation.html', {
                            "message": email_message,
                            "user": get_email,
                            "app_install": True,
                            "android_link": android_link,
                            "ios_link": ios_link,
                        })
                        msg = EmailMultiAlternatives(subject, text_content, DEFAULT_FROM_EMAIL, [get_email])
                        msg.attach_alternative(html_content, "text/html")

                        try:
                            msg.send()
                            return Response({'success': 'Email sent'})

                        except Exception as e:
                            return Response({'error': 'Email can not sent'})

            if mobile != '':
                try:
                    get_user = UserProfile.objects.get(email=mobile)
                    user = UserProfile.objects.get(user=get_user)
                    sms = 'You are invited to join the group' f' {gp.name} ' 'for the event' f' {event.name}'
                    notification_type = 'group_invitation'
                    get_user_event = Event.objects.get(id=gp.event_id)
                    message = 'You have got an invitation to join the group' f' {gp.name}'

                    # creating notification
                    kwargs = {'user': user, 'notification_type': notification_type, 'message': message,
                              'event': get_user_event, 'group': gp}
                    create_notification(**kwargs)
                except Exception as e:
                    print(e)
                    android_link = "https://play.google.com/store/apps/details?id=com.local_mingle"
                    ios_link = ""
                    sms = 'You are invited to join Local-mingle application. Below Android Link : \n' \
                          + android_link + '\n for android users. And Ios Link : \n' + ios_link + '\n for ' \
                          'ios users.\n you can install it and register for free.'

                import os
                from twilio.rest import Client

                # Find your Account SID and Auth Token at twilio.com/console
                # and set the environment variables. See http://twil.io/secure
                account_sid = TWILIO_ACCOUNT_SID
                auth_token = TWILIO_AUTH_TOKEN
                client = Client(account_sid, auth_token)
                try:
                    message = client.messages.create(body=sms,
                                                     from_='+13237451893',
                                                     to='+91'+mobile)
                    print(message.sid)
                    return Response({'success': 'SMS sent'})

                except Exception as e:
                    return Response({'error': 'SMS can not sent'})
                    pass

        else:
            return Response({'error': 'Group can not be blank'})


class GroupMessageListCreateView(ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GroupMessageSerializer
    queryset = GroupMessage.objects.all()

    def get_queryset(self):

        # Showing only that group which events are present today-onwards
        try:
            group_id = self.request.query_params['group_id']
            queryset = GroupMessage.objects.filter(Q(receiver=group_id),
                                                   receiver__event__date__gte=datetime.today()).order_by('id')
        except:
            if self.request.user:
                user_id = self.request.user.id
                get_unique_group = GroupMessage.objects.filter(Q(sender=user_id)).order_by('id')

                # logic to get latest message from group-message
                get_message_id = []
                get_receiver_id = []
                for q in get_unique_group:
                    if q.receiver not in get_receiver_id:
                        get_receiver_id.append(q.receiver)
                        get_message_id.append(q.id)
                queryset = GroupMessage.objects.filter(id__in=get_message_id,
                                                       receiver__event__date__gte=datetime.today()).order_by('id')

            else:
                queryset = self.queryset

        return queryset


class RecurringEventChangeApiView(APIView):

    def get(self, request):
        event_availability = Event.objects.all()

        if event_availability.exists():
            for event in event_availability:
                event_recurring = Event.objects.filter(name=event.name, event_status=event.event_status, venue=event.venue)
                event_count = event_recurring.count()

                if event_count > 1:
                    for ev in event_recurring:
                        same_event = Event.objects.filter(global_id=ev.global_id, venue=ev.venue)
                        same_event_count = same_event.count()

                        if same_event_count > 1:
                            for i, sm_event in enumerate(same_event):
                                j = same_event_count - 2
                                if i <= j:
                                    sm_event.delete()

                    base_id = None
                    event_recurring = Event.objects.filter(name=event.name, event_status=event.event_status, venue=event.venue)
                    event_count = event_recurring.count()
                    if event_count > 1:
                        for i, event_rec in enumerate(event_recurring):
                            if i == 0:
                                event_rec.recurring = True
                                base_id = event_rec.id
                                event_rec.save()
                            else:
                                recurring_event = RecurringEvent(event_id=base_id, time=event_rec.time,
                                                                 date=event_rec.date)
                                recurring_event.save()
                                event_rec.delete()

                else:
                    pass

            return Response({"success": True})


class RecurringEventViewSet(viewsets.ModelViewSet):
    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)
    serializer_class = RecurringEventSerializer
    queryset = RecurringEvent.objects.all()
    filterset_fields = {'event': ['exact'],
                        'event__id': ['exact'],
                        'date': ['gte', 'lte', 'exact']}

    def get_queryset(self):
        queryset = RecurringEvent.objects.filter(event__date__gte=datetime.today())
        return queryset


class GroupInvitationViewset(viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GroupInvitationSerializer
    queryset = GroupInvitation.objects.all()
    filterset_fields = {'group': ['exact'],
                        'group__id': ['exact'],
                        'status': ['exact']
                        }


class EventLatLongApiView(APIView, PageNumberPagination):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        lat = request.query_params.get('lat', '')
        long = request.query_params.get('long', '')
        city = request.query_params.get('city', '')
        state = request.query_params.get('state', '')
        postal_code = request.query_params.get('postal_code', '')
        date__gte = request.query_params.get('date__gte', '')
        date__lte = request.query_params.get('date__lte', '')
        category__parent_id = request.query_params.get('category__parent_id', '')
        if lat != '' and long != '':
            res = get_location(lat, long)  # getting venue results on the basis of lat-long

            # filtering the upcoming result in date range
            if date__lte != '' and date__gte != '':
                get_related_events = Event.objects.filter(venue__in=res, date__gte=date__gte, date__lte=date__lte
                                                          ).order_by('-id')

            # filtering the upcoming result in date range
            elif date__lte != '' and date__gte != '' and category__parent_id != '':
                get_related_events = Event.objects.filter(venue__in=res, date__gte=date__gte, date__lte=date__lte,
                                                          category__parent_id=category__parent_id).order_by('-id')

            # showing same results if date range and category is not found
            else:
                get_related_events = Event.objects.filter(venue__in=res, date__gte=datetime.today()).order_by('-id')

            # creating page instance for pagination
            queryset = get_related_events
            page = self.paginate_queryset(queryset, request)
            serializer = EventSerializer(
                page, many=True
            )
            return self.get_paginated_response(serializer.data)
        else:
            if city != "":
                queryset = Event.objects.filter(venue__city__iexact=city, date__gte=datetime.today()).order_by('-id')
                page = self.paginate_queryset(queryset, request)
                serializer = EventSerializer(
                    page, many=True
                )
                return self.get_paginated_response(serializer.data)
            elif state != "":
                queryset = Event.objects.filter(venue__state_name__iexact=state, date__gte=datetime.today()).order_by('-id')
                page = self.paginate_queryset(queryset, request)
                serializer = EventSerializer(
                    page, many=True
                )
                return self.get_paginated_response(serializer.data)
            elif postal_code != "":
                queryset = Event.objects.filter(venue__postal_code__iexact=postal_code, date__gte=datetime.today()).order_by('-id')
                page = self.paginate_queryset(queryset, request)
                serializer = EventSerializer(
                    page, many=True
                )
                return self.get_paginated_response(serializer.data)
            else:
                return Response({'error': 'Please add lat and long or city or state or postal_code in params'})


# crud for Message-setting
class MessageSettingViewSet(viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MessageSettingSerializer
    queryset = MessageSetting.objects.all()
    filterset_fields = ['sender__id', 'receiver__id', 'gp_receiver__id', 'block']


class CommentUserStackApiView(APIView, PageNumberPagination):
    def get(self, request):
        event = self.request.query_params.get('event_id', '')
        if event != '':
            event_comment = Comment.objects.filter(event_id=event)
            cr = []
            result = []

            # getting all the comments user wise and returning it in result list
            for ec in event_comment:
                if ec.created_by:
                    if ec.created_by_id not in cr:
                        cr.append(ec.created_by_id)
                        result.append(Comment.objects.filter(created_by_id=ec.created_by_id).order_by('-id'))

            # stacking comments user wise in data list
            data = []
            for i, j in enumerate(result):
                serializer = CommentSerializer(result[i], many=True)
                data.append({'id': i, 'comments': serializer.data})
            page = self.paginate_queryset(data, request)
            return self.get_paginated_response(page)
        else:
            return Response({'error': 'Please add event_id in query_params'})


class AcceptRejectGroupInvitation(APIView):
    # permission_classes = (permissions.AllowAny, )

    def get(self, request):
        get_status = self.request.query_params.get('status', '')
        notification = self.request.query_params.get('notification', '')
        if get_status != '' and notification != '':
            if get_status == "accepted":
                get_notification = Notification.objects.get(id=notification)
                create_member = Group.member.through.objects.create(group_id=get_notification.group_id,
                                                                    user_id=get_notification.user_id)
                get_user = User.objects.filter(id=get_notification.user_id)
                if get_user:
                    user = User.objects.get(id=get_notification.user_id)
                    group_invitation_instance = GroupInvitation.objects.filter(group_id=get_notification.group_id,
                                                                               invited_to=user.email)
                    if group_invitation_instance:
                        group_invitation_instance.update(status='accepted')
                else:
                    pass
                if create_member:
                    get_notification = Notification.objects.filter(id=notification)
                    get_notification.update(message='You have accepted the group invitation', accepted=True)

                return Response({'status': status.HTTP_201_CREATED, 'success': True})

            else:
                get_notification = Notification.objects.filter(id=notification)
                get_notification.update(message='You have rejected the group invitation', accepted=False)
                get_user = User.objects.filter(id=get_notification.user_id)
                if get_user:
                    user = User.objects.get(id=get_notification.user_id)
                    group_invitation_instance = GroupInvitation.objects.filter(group_id=get_notification.group_id,
                                                                               invited_to=user.email)
                    if group_invitation_instance:
                        group_invitation_instance.update(status='rejected')
                else:
                    pass
            return Response({'status': "rejected"})

        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'error': "Fields can not be blank"})


class PrimeOrLocalEventApiView(APIView, PageNumberPagination):

    def get(self, request):
        lat = request.query_params.get('lat', '')
        long = request.query_params.get('long', '')
        source = request.query_params.get('source', '')
        location = request.query_params.get('location', '')
        if lat != '' and long != '' and source != '':
            res = get_location(lat, long)  # getting venue results on the basis of lat-long

            # get_related_events = Event.objects.filter(Q(venue__in=res, date__gte=datetime.today()) |
            #                                           Q(source=source, date__gte=datetime.today())).order_by('-id')

            get_related_events = Event.objects.filter(venue__in=res, date__gte=datetime.today(),
                                                      source=source).order_by('-id')
            if get_related_events:
                queryset = get_related_events
            else:
                if location != '':
                    get_event = Event.objects.filter(date__gte=datetime.today())
                    queryset = get_event.filter(Q(venue__city__istartswith=location) | Q(venue__state_name__istartswith=location)
                                       | Q(venue__postal_code__istartswith=location)).order_by('-id')
                else:
                    return Response({'error': 'Please add location in params'})

            # creating page instance for pagination

            page = self.paginate_queryset(queryset, request)
            serializer = EventSerializer(
                page, many=True
            )
            return self.get_paginated_response(serializer.data)
        else:
            return Response({'error': 'Please add lat, long and source in params'})


class EventLocationApiView(APIView, PageNumberPagination):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        location = request.query_params.get('location', '')
        page = None
        if location != "":
            city = Event.objects.filter(venue__city__iexact=location, date__gte=datetime.today()).order_by('-id')
            state = Event.objects.filter(venue__state_name__iexact=location, date__gte=datetime.today()).order_by('-id')
            postal = Event.objects.filter(venue__postal_code__iexact=location, date__gte=datetime.today()).order_by('-id')
            if city:
                page = self.paginate_queryset(city, request)
            elif state:
                page = self.paginate_queryset(state, request)
            else:
                page = self.paginate_queryset(postal, request)

            serializer = EventSerializer(
                page, many=True
            )
            return self.get_paginated_response(serializer.data)
        else:
            return Response({'error': 'Please add location in query params'})


class EventLocationAutoSuggestApiView(APIView, PageNumberPagination):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        query = request.query_params.get('q', '')
        if query != "" and len(query) >= 2:
            get_ven = Venue.objects.filter(Q(city__icontains=query) | Q(state_name__icontains=query)).values_list(
                'city', 'state_name').distinct()[:7]
            venue = []
            for ven in get_ven:
                if ven[0] != "":
                    venue.append(ven[0])
                if ven[1] != "":
                    venue.append(ven[1])

            return Response(set(venue))
        else:
            return Response({'error': 'Please add q in query params'})


class GetMemberApiView(APIView, PageNumberPagination):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GetGroupMemberSerializer

    def get(self, request):
        group = self.request.query_params.get('group_id', None)

        if group:
            queryset = Group.objects.filter(id=group, event__date__gte=datetime.today())
            page = self.paginate_queryset(queryset, request)
            serializer = GetGroupMemberSerializer(
                page, many=True
            )
            return self.get_paginated_response(serializer.data)
        else:
            return Response({'error': 'Please pass group_id in parameters'})
