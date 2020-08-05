from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, make_random_password
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import math
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import errand_matcher.helper as helper
from errand_matcher.models import Errand
from errand_matcher.models import User, Volunteer, Requestor, UserOTP
from errand_matcher.models import SiteConfiguration
import phonenumbers
import uuid
from datetime import timedelta

frequency_choice_lookup = {
    'Anytime': 1,
    '2-3 times a week': 2,
    'Once a week': 3
}

contact_choice_lookup = {
    'SMS text': 1,
    'Phone call': 2
}

def index(request):
    return render(request, 'errand_matcher/index.html')

def health_and_safety(request):
    return render(request, 'errand_matcher/health-and-safety.html')

def error(request):
    return render(request, 'errand_matcher/404.html', {'base_url': helper.get_base_url()})

@csrf_exempt
def sms_inbound(request):
    from_number = request.POST['From']
    body = request.POST['body']

    # forward text to on-call staffer
    message = '{}: {}'.format(from_number, body)
    helper.send_sms(helper.format_mobile_number(helper.get_support_mobile_number()), message)
    return

def volunteer(request):
    return render(request, 'errand_matcher/volunteer.html')

def volunteer_login(request):
    if request.method == 'POST':
        mobile_number_str = request.POST.get('phone-input')

        # Is mobile number associated with Volunteer?
        volunteer = helper.get_volunteer_from_mobile_number_str(mobile_number_str)

        # If Volunteer found, create OTP
        if volunteer is not None:
            user_otp = UserOTP.objects.create(mobile_number = volunteer.mobile_number)

            # deliver OTP
            message = "Livelyhood here! {} is your one-time password for online login. Please do not share.".format(
                user_otp.token)
            helper.send_sms(helper.format_mobile_number(user_otp.mobile_number), message)
            
            return render(request, 'errand_matcher/volunteer-login-otp.html')
        # If no Volunteer found, show warning and redirect back to signup
        else:
            return render(request, 'errand_matcher/volunteer-login.html', {
                'warning': 'Not found'})
            
    else:
        return render(request, 'errand_matcher/volunteer-login.html')

def volunteer_login_otp(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp-input')
        user_otp = UserOTP.objects.filter(token=otp_input).first()

        # If OTP found, login
        if user_otp is not None:
            volunteer = Volunteer.objects.filter(mobile_number=user_otp.mobile_number).first()
            user = authenticate(request, username = volunteer.email_address, 
                    password = helper.strip_mobile_number(volunteer.mobile_number))
            # Redirect to a success page if authenticated
            if user is not None:
                login(request, user)
            # Else an 'invalid login' error message.
            else:
                pass
        
        # If OTP not found, show warning and redirect back to signup
        else:
            return render(request, 'errand_matcher/volunteer-login-otp.html', {
                'warning': 'Not found'
                })

    else:
        return render(request, 'errand_matcher/volunteer-login-otp.html')


def volunteer_signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        mobile_number = request.POST['mobile_number']
        frequency = request.POST['frequency']
        language = request.POST.get('language', '')
        transportation = request.POST['transportation']
        lat = request.POST['lat']
        lon = request.POST['lon']

        user = User(username=email, 
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=make_password(mobile_number),
            user_type=1)
        user.save()

        freq_no = frequency_choice_lookup[frequency]

        walks = False
        has_bike = False
        has_car = False
        transportation_arr = transportation.split(', ')
        if "My own two feet" in transportation_arr:
            walks = True
        if "Bike" in transportation_arr:
            has_bike = True
        if "Car" in transportation_arr:
            has_car = True

        speaks_spanish = False
        speaks_russian = False
        speaks_chinese = False

        if len(language) > 0:
            language_arr = language.split(', ')

            if "Spanish" in language_arr:
                speaks_spanish = True
            if "Russian" in language_arr:
                speaks_russian = True
            if "Chinese" in language_arr:
                speaks_chinese = True

        volunteer = Volunteer(
            user=user,
            # PhoneNumberField requires country code
            mobile_number='+1' + mobile_number,
            lon=lon,
            lat=lat,
            frequency=freq_no,
            walks=walks,
            has_bike = has_bike,
            has_car = has_car,
            speaks_spanish = speaks_spanish,
            speaks_russian = speaks_russian,
            speaks_chinese = speaks_chinese,
            consented = True)
        volunteer.save()

        tiny_faq_url = helper.make_tiny_url("{}#above-faq".format(helper.get_base_url()))
        message = "Thanks for signing up to help make deliveries for at-risk members of your community!"\
        " We'll text you when someone nearby needs your help. In the meantime, you can get ready by reading our FAQs:{}"\
        " . And if you ever need help, you can always text us here.\n"\
        "Reply STOP to stop receiving notifications of new requests.".format(tiny_faq_url)
        helper.send_sms(helper.format_mobile_number(volunteer.mobile_number), message)

        return HttpResponse(status=204)
    else:
        return render(request, 'errand_matcher/volunteer-signup.html',
            {'GMAPS_API_KEY': os.environ.get('GMAPS_API_KEY')})

def requestor(request):
    return render(request, 'errand_matcher/requestor-request.html')

def requestor_login(request):
    if request.method == 'POST':
        mobile_number = request.POST.get('phone-input')
        dob = request.POST.get('dob-input')
        parsed_mobile_number = phonenumbers.parse('+1{}'.format(mobile_number))
        requestor = Requestor.objects.filter(mobile_number=parsed_mobile_number, 
            date_of_birth=dob).first()

        # Requestor not found, sign up
        if requestor is None:
            return render(request, 'errand_matcher/requestor-signup.html',
             {'GMAPS_API_KEY': os.environ.get('GMAPS_API_KEY'),
             'mobile_number': mobile_number,
             'date_of_birth': dob})
        
        else:
            return render(request, 'errand_matcher/request-errand.html', 
                {'requestor_number': mobile_number})
    else:
        return render(request, 'errand_matcher/requestor-login.html')

def requestor_signup(request):
    if request.method == 'POST':
        first_name = request.POST['firstname-review']
        last_name = request.POST['lastname-review']
        mobile_number = request.POST['phone-review']
        contact_preference = request.POST['contact-review']
        date_of_birth = request.POST['dob-review']
        address = request.POST['address-review']

        # SV 4-10-20 : TODO language preference patch

        user = User(username=mobile_number, 
            first_name=first_name,
            last_name=last_name,
            email='',
            password=make_password(date_of_birth),
            user_type=2)
        user.save()

        coord_location = helper.gmaps_geocode(address)

        requestor = Requestor(
            user=user,
            # PhoneNumberField requires country code
            mobile_number='+1' + mobile_number,
            date_of_birth=date_of_birth,
            lon=coord_location['lng'],
            lat=coord_location['lat'],
            contact_preference = contact_choice_lookup[contact_preference])
        requestor.save()
        return render(request, 'errand_matcher/request-errand.html', 
                {'requestor_number': mobile_number, 'requestor_name': first_name})

    else:
        return render(request, 'errand_matcher/requestor-signup.html',
            {'GMAPS_API_KEY': os.environ.get('GMAPS_API_KEY')})

def request_errand(request):
    if request.method == 'POST':
        requestor_number = request.POST['requestor_number']
        additional_info = request.POST['additional_info']
        urgency = request.POST['urgency']
        requestor = helper.get_user_from_mobile_number_str(requestor_number, 'requestor')

        errand = Errand(
            requested_time = timezone.now(),
            status = 1,
            due_by = helper.calculate_errand_deadline(urgency),
            requestor = requestor,
            additional_info = additional_info
        )
        errand.save()

        return HttpResponse(status=204)
    else:
        return render(request, 'errand_matcher/request-errand.html')

def accept_errand(request, errand_id, volunteer_number):
    if request.method == 'POST':
        # To DO: what if errand isn't open?
        errand = Errand.objects.get(id=errand_id)
        volunteer = helper.get_volunteer_from_mobile_number_str(volunteer_number)

        # update errand
        errand.status = 2
        errand.claimed_time = timezone.now()
        errand.claimed_volunteer = volunteer
        errand.access_id = uuid.uuid4()
        errand.save()

        # send text to volunteer with unique link
        url = "{}/errand/{}/status/{}".format(helper.get_base_url(), errand.id, errand.access_id)
        message = "Thanks for accepting this request! See details at {}".format(url)
        helper.send_sms(helper.format_mobile_number(volunteer.mobile_number), message)
        return HttpResponse(status=204)

    else:
        # TO DO: verify that volunteer is associated with errand
        errand = Errand.objects.get(id=errand_id)
        volunteer = helper.get_volunteer_from_mobile_number_str(volunteer_number)
        
        # TO DO: failure case if no modes
        modes = []
        if volunteer.walks:
            modes.append('walking')
        if volunteer.has_bike:
            modes.append('bicycling')
        if volunteer.has_car:
            modes.append('driving')

        distances = helper.gmaps_distance((volunteer.lat, volunteer.lon), 
            (errand.requestor.lat, errand.requestor.lon), modes)
        if len(distances) == 1:
            distance_str = distances[0][1] + ' ' + distances[0][0]
        else:
            last_item = distances.pop()
            distance_str = ''
            for distance_mode, distance_duration in distances:
                distance_str = distance_str + distance_duration + ' ' + distance_mode + ', '
            distance_str = distance_str + 'or ' + last_item[1] + ' ' + last_item[0]

        deadline_str = helper.convert_errand_deadline_to_str(errand)

        address = helper.gmaps_reverse_geocode((errand.requestor.lat, errand.requestor.lon))

        requestor_number = helper.format_mobile_number(errand.requestor.mobile_number)

        contact_preference = 'Texting' if errand.requestor.contact_preference == 1 else 'Phone call'

        # on-staff number
        site_configuration = SiteConfiguration.objects.first()
        staff_number = phonenumbers.format_number(
            site_configuration.mobile_number_on_call, phonenumbers.PhoneNumberFormat.NATIONAL)

        return render(request, 'errand_matcher/errand-accept.html', {
            'requestor': errand.requestor,
            'errand_deadline': deadline_str,
            'distance': distance_str,
            'errand_status': errand.status,
            'additional_info': errand.additional_info,
            'contact_preference': contact_preference,
            'address': address,
            'requestor_number': requestor_number,
            'staff_number': staff_number,
            'base_url': helper.get_base_url()
            })

def view_errand(request, errand_id, access_id):
    errand = Errand.objects.filter(access_id=access_id).first()
    errand_expiration_hours = math.floor((errand.due_by - timezone.now()).total_seconds() / 3600)
    contact_preference = 'Texting' if errand.requestor.contact_preference == 1 else 'Phone call'
    address = helper.gmaps_reverse_geocode((errand.requestor.lat, errand.requestor.lon))
    requestor_number = helper.format_mobile_number(errand.requestor.mobile_number)
    if errand is not None:
        return render(request, 'errand_matcher/errand-view.html', {
            'errand_number': int(errand.id),
            'requestor': errand.requestor,
            'time_left': errand_expiration_hours,
            'additional_info': errand.additional_info,
            'contact_preference': contact_preference,
            'address': address,
            'requestor_number': requestor_number,
            'base_url': helper.get_base_url()
            })

    else:
        return render(request, 'errand_matcher/404.html', {'base_url': helper.get_base_url()})

def partner(request):
    if request.method == 'POST':
        username = request.POST['partners-login-email']
        password = request.POST['partners-login-password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/partner/dashboard/')
        else:
            pass
            # Return an 'invalid login' error message.
    else:
        return render(request, 'errand_matcher/partner.html')

def partner_request(request):
    if request.method == 'POST':
        requestor_number = request.POST['add-requestor-phone']
        requestor = helper.get_user_from_mobile_number_str(requestor_number, user_type='requestor')
        if requestor is None:
            requestor_first_name = request.POST['add-requestor-first-name']
            requestor_last_name = request.POST['add-requestor-last-name']
            requestor_address = request.POST['add-requestor-address']
            requestor_apartment = request.POST['add-requestor-apartment']

            user = User(
                username=requestor_number,
                first_name=requestor_first_name,
                last_name=requestor_last_name,
                email='',
                password=User.objects.make_random_password(),
                user_type=2)
            user.save()

            coord_location = helper.gmaps_geocode(requestor_address)

            requestor = Requestor(
                user=user,
                mobile_number='+1' + requestor_number,
                lon=coord_location['lng'],
                lat=coord_location['lat'],
                address_str = requestor_address,
                apt_no = requestor_apartment,
                # Default to calling as contact preference
                contact_preference = 'call')
            requestor.save()
        else:
            user = requestor.user
            user.first_name = requestor_first_name
            user.last_name = requestor_last_name
            user.save()


def partner_password_reset(request):
    pass

def partner_password_reset_done(request):
    pass

def partner_reset_confirm(request, token):
    pass

def partner_reset_complete(request):
    pass

@login_required(login_url='/partner/')
def partner_dashboard(request):
    errands = Errand.objects.filter(affiliated_partner=request.user.partner)
    return render(request, 'errand_matcher/partner-dashboard.html', {'errands': errands})

