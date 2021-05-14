from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from rest_framework import authentication, permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.custom_mixin import QuerySetFilterMixin
from event.models import Event, Category, Venue, Comment, Like, Subscription, UserSubscription,\
    Follow, Message, Member, Group, EventGroup, EventSetting
from event.serializers import EventSerializer, CategorySerializer, VenueSerializer, UserSubscriptionSerializer, \
    CommentSerializer, LikeSerializer, SubscriptionSerializer, FollowSerializer, MessageSerializer, MemberSerializer,\
    GroupSerializer, EventGroupSerializer, EventSettingSerializer, GroupMemberSerializer

from event.ticketmaster import GetEventList

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
                        }


# to create events' category
class CategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


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
                        if event_availability.exists():
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
                                                   date=event.local_start_date, description='')
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
    filterset_fields = ['event__id']


# crud for like
class LikeViewSet(QuerySetFilterMixin, viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LikeSerializer
    queryset = Like.objects.all()


# crud for subscription
class SubscriptionViewSet(QuerySetFilterMixin, viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


# crud for User subscription
class UserSubscriptionViewSet(QuerySetFilterMixin, viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSubscriptionSerializer
    queryset = UserSubscription.objects.all()


class FollowViewSet(QuerySetFilterMixin, viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()


class MessageViewSet(QuerySetFilterMixin, viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MessageSerializer
    queryset = Message.objects.all()


class MemberViewSet(QuerySetFilterMixin, viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MemberSerializer
    queryset = Member.objects.all()


class GroupViewSet(QuerySetFilterMixin, viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


class GroupMemberViewSet(QuerySetFilterMixin, viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GroupMemberSerializer
    queryset = Group.objects.all()
    filterset_fields = ['id']


class EventGroupViewSet(QuerySetFilterMixin, viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EventGroupSerializer
    queryset = EventGroup.objects.all()
    filterset_fields = ['event__id', 'group__id']


class EventSettingViewSet(QuerySetFilterMixin, viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EventSettingSerializer
    queryset = EventSetting.objects.all()
