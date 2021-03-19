from event.models import Event, Category, Venue
from utils.custom_mixin import QuerySetFilterMixin, CustomBaseSerializer


class EventSerializer(CustomBaseSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class CategorySerializer(CustomBaseSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class VenueSerializer(CustomBaseSerializer):
    class Meta:
        model = Venue
        fields = '__all__'
