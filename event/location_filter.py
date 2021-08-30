from event.models import Venue
from geopy.distance import great_circle
from local_mingle_backend.settings import MILE_LOCATION


def get_venue(lat, long):
    venue = Venue.objects.all()
    for ven in venue:
        if ven.latitude != "":
            print(ven.id)
            if -90 < float(ven.latitude) < 90:
                ven_location = (ven.latitude, ven.longitude)
                user_location = (long, lat)
                get_miles = great_circle(user_location, ven_location).miles
                if get_miles <= MILE_LOCATION:
                    yield ven
            else:
                ven_location = (ven.longitude, ven.latitude )
                user_location = (lat, long)
                get_miles = great_circle(user_location, ven_location).miles
                if get_miles <= MILE_LOCATION:
                    yield ven


def get_location(lat, long):
    venue = []
    for ven in get_venue(lat, long):
        venue.append(ven)
    return venue


