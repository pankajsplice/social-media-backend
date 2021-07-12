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
    RecurringEventSerializer, GroupInvitationSerializer, MessageSettingSerializer

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
                        }

    def get_queryset(self):
        queryset = Event.objects.filter(date__gte=datetime.today())
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
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    filterset_fields = ['event__id', 'created_by__id']

    def get_queryset(self):
        queryset = super().get_queryset()
        event_filter = self.request.query_params.get('event__id', '')
        if event_filter != '':
            queryset = super().get_queryset().order_by('-created_by')
        return queryset


# crud for like
class LikeViewSet(QuerySetFilterMixin, viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    filterset_fields = ['event__id', 'created_by__id']


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
            queryset = Group.objects.filter(Q(member=self.request.user) | Q(created_by=self.request.user))
            return queryset
        else:
            return self.queryset


class EventSettingViewSet(QuerySetFilterMixin, viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EventSettingSerializer
    queryset = EventSetting.objects.all()
    filterset_fields = {'event__name': ['iexact', 'istartswith'],
                        'event': ['exact'],
                        'going': ['exact'],
                        'user__id': ['exact']}


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
            profile = UserProfile.objects.get(user=i.id)
            serializer_profile = UserProfileSerializer(profile)
            print(profile.profile_pic)
            user = serializer.data
            user['profile'] = serializer_profile.data
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
        messages1 = Message.objects.filter(sender=user, receiver=friend).order_by('id')
        messages2 = Message.objects.filter(sender=friend, receiver=user).order_by('id')
        print(messages1, messages2)
        messages = []
        if len(messages1) + len(messages2) >= 2:
            for i in range(len(messages1) + len(messages2)):
                try:
                    serializer1 = MessageSerializer(messages1[i])
                    messages.append(serializer1.data)
                except:
                    pass
                try:
                    serializer2 = MessageSerializer(messages2[i])
                    messages.append(serializer2.data)
                except:
                    pass
        else:
            if len(messages1) >= 1:
                serializer1 = MessageSerializer(messages1[0])
                messages.append(serializer1.data)
            if len(messages2) >= 1:
                serializer2 = MessageSerializer(messages2[0])
                messages.append(serializer2.data)
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
                user = User.objects.get(email=get_email)
                if user:
                    email_message = 'You are invited to join the group' f' {gp.name} ' 'for the event' f' {event.name}'

                    subject = 'LocalMingle Group Invitation'
                    text_content = ''
                    html_content = render_to_string('mail/group_invitation.html', {
                        "message": email_message,
                        "user": f"{user.first_name} {user.last_name}",
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

                else:
                    subject = 'LocalMingle Group Invitation'
                    text_content = ''
                    email_message = 'You are invited to join Local-mingle application. Here is the link you can ' \
                                    'install it and register for free. '
                    html_content = render_to_string('mail/group_invitation.html', {
                        "message": email_message,
                        "user": get_email,
                    })
                    msg = EmailMultiAlternatives(subject, text_content, DEFAULT_FROM_EMAIL, [get_email])
                    msg.attach_alternative(html_content, "text/html")

                try:
                    # send_mail(subject='Invitation Link', message=email_message, from_email=DEFAULT_FROM_EMAIL,
                    #           recipient_list=[get_email], fail_silently=True)
                    msg.send()
                    return Response({'success': 'Email sent'})

                except Exception as e:
                    return Response({'error': 'Email can not sent'})

            if mobile != '':
                user = User.objects.get(email=get_email)
                if user:
                    sms = 'You are invited to join the group' f' {gp.name} ' 'for the event' f' {event.name}'
                    notification_type = 'group_invitation'
                    get_user_event = Event.objects.get(id=gp.event_id)
                    message = 'You have got an invitation to join the group' f' {gp.name}'

                    # creating notification
                    kwargs = {'user': user, 'notification_type': notification_type, 'message': message,
                              'event': get_user_event, 'group': gp}
                    create_notification(**kwargs)
                else:
                    sms = 'You are invited to join Local-mingle application. Here is the link you can install it ' \
                              'and register for free. '

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
        try:
            group_id = self.request.query_params['group_id']
            queryset = GroupMessage.objects.filter(Q(receiver=group_id),
                                                   receiver__event__date__gte=datetime.today()).order_by('-id')
        except:
            if self.request.user:
                user_id = self.request.user.id
                get_unique_group = GroupMessage.objects.filter(Q(sender=user_id)).order_by('-id')

                # logic to get latest message from group-message
                get_message_id = []
                get_receiver_id = []
                for q in get_unique_group:
                    if q.receiver not in get_receiver_id:
                        get_receiver_id.append(q.receiver)
                        get_message_id.append(q.id)
                queryset = GroupMessage.objects.filter(id__in=get_message_id,
                                                       receiver__event__date__gte=datetime.today()).order_by('-id')

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
    filterset_fields = ['sender__id', 'receiver__id', 'block']


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

