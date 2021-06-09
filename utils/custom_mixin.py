from django.db.models import Q
from rest_framework import serializers
from event.notifications import create_notification
from event.models import Category, Event, Venue
from django.contrib.auth.models import User


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


class QuerySetFilterMixin(object):
    def get_queryset(self):
        # This query is okay for Organization user
        # this query return data based on created by and mapped to related organization

        if self.request.user.is_superuser:
            queryset = super().get_queryset()
            return queryset

        # queryset = super().get_queryset().filter(Q(created_by=self.request.user))
        queryset = super().get_queryset()
        return queryset

    def perform_create(self, serializer):
        if self.basename == 'event':
            if self.request.data['user'] or self.request.data['created_by'] or self.request.data['updated_by']:
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
                    event_instance = serializer.save(created_by_id=int(self.request.data['created_by']),
                                                     updated_by_id=int(self.request.data['created_by']),
                                                     category_id=prime_category, venue_id=venue_id)
                    if event_instance:
                        notification_type = self.basename
                        event = event_instance
                        user = event_instance.created_by
                        message = 'Your event has been created.'
                        # creating notification
                        kwargs = {'user': user, 'notification_type': notification_type, 'message': message, 'event': event}
                        create_notification(**kwargs)

        if self.basename == 'like':
            notification_type = self.basename
            event = self.request.data['event']
            get_user_event = Event.objects.get(id=event)
            user = get_user_event.created_by
            message = 'You have get a like on your event'

            # creating notification
            kwargs = {'user': user, 'notification_type': notification_type, 'message': message, 'event': get_user_event}
            create_notification(**kwargs)
            serializer.save(created_by=self.request.user, updated_by=self.request.user)

        if self.basename == 'comment':
            notification_type = self.basename
            event = self.request.data['event']
            get_user_event = Event.objects.get(id=event)
            user = get_user_event.created_by
            message = 'A new person is commented on your event'

            # creating notification
            kwargs = {'user': user, 'notification_type': notification_type, 'message': message, 'event': get_user_event}
            create_notification(**kwargs)
            serializer.save(created_by=self.request.user, updated_by=self.request.user)

        if self.basename == 'follow':
            notification_type = self.basename
            event = self.request.data['event']
            get_user_event = Event.objects.get(id=event)
            user = get_user_event.created_by
            message = 'A new person is followed your event'

            # creating notification
            kwargs = {'user': user, 'notification_type': notification_type, 'message': message, 'event': get_user_event}
            create_notification(**kwargs)
            serializer.save(created_by=self.request.user, updated_by=self.request.user)

        if self.basename == 'event_group':
            user = self.request.user
            notification_type = self.basename
            event = self.request.data['event']
            event_obj = Event.objects.get(id=event)
            message = 'Your group is created'

            # creating notification
            kwargs = {'user': user, 'notification_type': notification_type, 'message': message, 'event': event_obj}
            create_notification(**kwargs)
            serializer.save(created_by=self.request.user, updated_by=self.request.user)

        if self.basename == 'message':
            # user = self.request.user
            notification_type = self.basename
            event = self.request.data['event']
            get_user_event = Event.objects.get(id=event)
            user = get_user_event.created_by
            sender = self.request.data['sender']
            message = 'You have received a new message '
            # creating notification
            kwargs = {'user': user, 'notification_type': notification_type, 'message': message, 'event': get_user_event}
            create_notification(**kwargs)
            serializer.save(created_by=self.request.user, updated_by=self.request.user)

        else:
            serializer.created_by = self.request.user
            serializer.updated_by = self.request.user
            serializer.save()

    def perform_update(self, serializer):
        if self.basename == 'event':
            user = self.request.data['created_by']
            notification_type = self.basename
            event = self.request.parser_context['kwargs']['pk']
            message = 'Your event has been updated'
            get_user = User.objects.get(id=int(user))
            event_object = Event.objects.get(id=int(event))

            # creating notification
            kwargs = {'user': get_user, 'notification_type': notification_type, 'message': message, 'event': event_object}
            create_notification(**kwargs)

            serializer.save(updated_by_id=int(self.request.data['updated_by']))

        else:
            serializer.updated_by = self.request.user
            serializer.save()


class CustomBaseSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        validated_data = dict(list(self.validated_data.items()) + list(kwargs.items()))
        print("validated_data: ", validated_data)
        # validated_data['updated_by'] = self.updated_by
        # validated_data['created_by'] = self.created_by

        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, (
                '`update()` did not return an object instance.'
            )
        else:
            # validated_data['created_by'] = self.created_by
            self.instance = self.create(validated_data)
            assert self.instance is not None, (
                '`create()` did not return an object instance.'
            )

        return self.instance
