from errand_matcher.models import Errand, Requestor, Volunteer
import math
import googlemaps
from urllib.parse import urlencode
from urllib.request import urlopen
import contextlib
from twilio.rest import Client
import os
from django.utils import timezone
from datetime import timedelta

def make_tiny_url(url):
    request_url = ('http://tinyurl.com/api-create.php?' + 
    urlencode({'url':url}))
    with contextlib.closing(urlopen(request_url)) as response:
        return response.read().decode('utf-8')

def send_sms(to_number, message):
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    twilio_number = os.environ.get('TWILIO_NUMBER')
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_=twilio_number,
        to=to_number)
    return

def match_errand_to_volunteers(errand):
    # exclude volunteers contacted on open errands
    volunteers_on_open_errands = []
    open_errands = Errand.objects.filter(status=1)
    for open_errand in open_errands:
        volunteers_on_open_errands = volunteers_on_open_errands + \
        list(open_errand.contacted_volunteers.all().values_list(
            'mobile_number', flat=True))
    # exclude volunteers already fulfilled preference
    errands_last_week = Errand.objects.filter(
        status__in=[2,3], 
        claimed_time__gte=timezone.now()-timedelta(days=7))

    history = {}
    for errand_last_week in errands_last_week:
        v = errand_last_week.claimed_volunteer
        if v.mobile_number in history:
            history[v.mobile_number]['errand_counter'] += 1
        else:
            history[v.mobile_number] = {
                'pref': v.frequency,
                'errand_counter': 1
            }

    volunteers_already_fulfilled_prefs = []
    for v, v_prefs in history.items():
        if v_prefs['pref'] == 1:
            continue
        if v_prefs['pref'] == 2:
            if v_prefs['errand_counter'] >= 3:
                volunteers_already_fulfilled_prefs.append(v)

        if v_prefs['pref'] == 3:
            volunteers_already_fulfilled_prefs.append(v)

    # find up to 5 closest volunteers to requestor
    eligible_volunteers = Volunteer.objects.exclude(
        mobile_number__in=volunteers_on_open_errands+volunteers_already_fulfilled_prefs)

    by_distance = sorted(eligible_volunteers, 
        key=lambda v: distance((v.lat,v.lon),(errand.requestor.lat,errand.requestor.lon)))

    return by_distance[:5] if len(by_distance) > 5 else by_distance

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

def gmaps_reverse_geocode(latlng):
   # Reference: https://github.com/googlemaps/google-maps-services-python/blob/master/googlemaps/distance_matrix.py
    gmaps = googlemaps.Client(key=os.environ.get('GMAPS_API_KEY'))

    gmaps_result = gmaps.reverse_geocode(latlng)
    # TO DO: error case
    return gmaps_result[0]['formatted_address']

def gmaps_geocode(address):
    gmaps = googlemaps.Client(key=os.environ.get('GMAPS_API_KEY'))

    gmaps_result = gmaps.geocode(address)
    # TO DO: error case
    return gmaps_result[0]['geometry']['location']


def gmaps_distance(origin, destination, modes):
    # Reference: https://github.com/googlemaps/google-maps-services-python/blob/master/googlemaps/distance_matrix.py
    gmaps = googlemaps.Client(key=os.environ.get('GMAPS_API_KEY'))

    distance_result = []
    for mode in modes:
        # Valid values are "driving", "walking", "transit" or "bicycling".
        gmaps_result = gmaps.distance_matrix(origin, destination, mode=mode, units='imperial')
        mode_duration = gmaps_result['rows'][0]['elements'][0]['duration']['text']
        distance_result.append((mode, mode_duration))

    return distance_result