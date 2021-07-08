from rest_framework import viewsets, permissions, authentication
from event.serializers import EventSerializer
from django_filters import rest_framework as filters
from event.models import Event, Category,Venue, Group
from event.notifications import create_notification
from django.contrib.auth.models import User
from datetime import datetime
from utils.custom_mixin import QuerySetFilterMixin
from django.db.models import Q


def create_manual_category(category, parent):
    category_obj = Category.objects.get(id=category)
    category_ins = None
    if category_obj:
        if category_obj.parent.name == 'Prime Events':
            return category_obj
        else:
            name = f"{'Prime'} {category_obj.name}"
            try:
                get_category = Category.objects.get(name=name)
                category_ins = get_category.id
            except:
                save_category = Category.objects.create(name=name, parent=parent)
                category_ins = save_category.id
    return category_ins


class QuerySetFilterMixinWeb(object):
    def get_queryset(self):

        if self.request.user.is_superuser:
            queryset = super().get_queryset().filter(date__gte=datetime.today())
            return queryset

        queryset = super().get_queryset().filter(Q(date__gte=datetime.today(), created_by=self.request.user))
        return queryset

    def perform_create(self, serializer):
        if self.basename == 'event':
            if self.request.user:
                get_category = Category.objects.get(name='Prime Events')
                event_category = self.request.data['category']
                prime_category = create_manual_category(event_category, get_category)
                venue_name = self.request.data['venue_name']
                venue_global_id = self.request.data['venue_global_id']
                venue_address = self.request.data['venue_address']
                longitude = self.request.data['longitude']
                latitude = self.request.data['latitude']
                venue_id = None
                try:
                    venue_ins = Venue.objects.get(name=venue_name)
                    venue_id = venue_ins.id

                except:
                    venue_ins = Venue(name=venue_name, global_id=venue_global_id, city='', address=venue_address,
                                      state_code='', state_name='', postal_code='', country_code='', country_name='',
                                      latitude=latitude, longitude=longitude)
                    venue_ins.save()
                    venue_id = venue_ins.pk

                if prime_category:
                    event_instance = serializer.save(created_by=self.request.user,
                                                     updated_by=self.request.user,
                                                     category_id=prime_category, venue_id=venue_id)
                    if event_instance:
                        notification_type = self.basename
                        event = event_instance
                        user = event_instance.created_by
                        message = 'Your event has been created.'
                        # creating notification
                        kwargs = {'user': user, 'notification_type': notification_type, 'message': message,
                                  'event': event, 'group': ''}
                        create_notification(**kwargs)

    def perform_update(self, serializer):
        if self.basename == 'event':
            user = self.request.user
            notification_type = self.basename
            event = self.request.parser_context['kwargs']['pk']
            message = 'Your event has been updated'
            get_user = User.objects.get(user)
            event_object = Event.objects.get(id=int(event))

            # creating notification
            kwargs = {'user': get_user, 'notification_type': notification_type, 'message': message,
                      'event': event_object, 'group': ''}
            create_notification(**kwargs)

            serializer.save(updated_by=user)

        else:
            serializer.updated_by = self.request.user
            serializer.save()


class EventWebViewSet(QuerySetFilterMixinWeb, viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
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

    # def get_queryset(self):
    #     queryset = Event.objects.filter(date__gte=datetime.today())
    #     return queryset
