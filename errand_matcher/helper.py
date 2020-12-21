from errand_matcher.models import Errand, Requestor, Volunteer, SiteConfiguration
import math
import googlemaps
from urllib.parse import urlencode
from urllib.request import urlopen
import contextlib
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
from django.utils import timezone
from datetime import timedelta
import phonenumbers

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
    try:
        message = client.messages.create(
            body=message,
            from_=twilio_number,
            to=to_number)
    except TwilioRestException as e:
        print(e)
    return


def get_base_url():
    url_lookup = {
        'LOCAL': 'http://127.0.0.1:8000',
        'STAGING': 'https://staging-shieldcovid.herokuapp.com',
        'PROD': 'https://www.livelyhood.io'
    }
    
    deploy_stage = os.environ.get('DEPLOY_STAGE')
    return url_lookup[deploy_stage]


def get_support_mobile_number():
    site_configuration = SiteConfiguration.objects.first()
    return site_configuration.mobile_number_on_call


def get_max_request_rounds():
    site_configuration = SiteConfiguration.objects.first()
    return site_configuration.max_request_rounds


def strip_mobile_number(mobile_number):
    mobile_number_str = format_mobile_number(mobile_number, 
        number_format=phonenumbers.PhoneNumberFormat.E164)
    mobile_number_stripped = mobile_number_str.replace('+1', '')
    return mobile_number_stripped


def format_mobile_number(mobile_number, number_format=phonenumbers.PhoneNumberFormat.NATIONAL):
    return phonenumbers.format_number(mobile_number, number_format)


def get_user_from_mobile_number_str(mobile_number_str, user_type='volunteer'):
    if len(mobile_number_str) == 12:
        parsed_mobile_number = mobile_number_str
    else:
        parsed_mobile_number = phonenumbers.parse('+1{}'.format(mobile_number_str))
    
    # TO DO: failure case if multiple users or DNE?
    if user_type == 'volunteer':
        volunteer = Volunteer.objects.filter(mobile_number=parsed_mobile_number).first()
        return volunteer
    else:
        requestor = Requestor.objects.filter(mobile_number=parsed_mobile_number).first()
        return requestor


def calculate_errand_deadline(deadline_str):
    days_to_add = {
        'In less than 24 hours': 1,
        'Within 3 days': 3
    }
    return timezone.now() + timedelta(days=days_to_add[deadline_str])


def convert_errand_deadline_to_str(errand):
    weekday_lookup = {
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday',
        7: 'Sunday'
    }
    deadline_str = '{} at 8 p.m.'.format(
        weekday_lookup[errand.due_by.date().isoweekday()])
    return deadline_str


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
        mobile_number__in=volunteers_on_open_errands+volunteers_already_fulfilled_prefs+[''])

    # confirm volunteers have valid phone numbers
    valid_phones = [ev for ev in eligible_volunteers if phonenumbers.is_valid_number(ev.mobile_number)]

    by_distance = sorted(valid_phones, 
        key=lambda v: distance((v.lat,v.lon),(errand.requestor.lat,errand.requestor.lon)))

    return by_distance[:5] if len(by_distance) > 5 else by_distance

def get_k_closest_errands_to_volunteer(volunteer, k=5):
    open_errands = Errand.objects.filter(status=1)
    # sort open errands by distance to volunteer, from smallest to largest
    sorted_open_errands = sorted(open_errands, key=lambda x: distance((x.requestor.lat, x.requestor.lon),(volunteer.lat,volunteer.lon)))
    return sorted_open_errands[:k] if len(sorted_open_errands) > k else sorted_open_errands


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

def get_volunteer_distance_to_errand(errand, volunteer):
    # TO DO: failure case if no modes
    modes = []
    if volunteer.walks:
        modes.append('walking')
    if volunteer.has_bike:
        modes.append('bicycling')
    if volunteer.has_car:
        modes.append('driving')

    distances = gmaps_distance((volunteer.lat, volunteer.lon), 
        (errand.requestor.lat, errand.requestor.lon), modes)
    if len(distances) == 1:
        distance_str = distances[0][1] + ' ' + distances[0][0]
    else:
        last_item = distances.pop()
        distance_str = ''
        for distance_mode, distance_duration in distances:
            distance_str = distance_str + distance_duration + ' ' + distance_mode + ', '
        distance_str = distance_str + 'or ' + last_item[1] + ' ' + last_item[0]

    return distance_str

        