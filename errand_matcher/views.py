from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
import inflect
import math
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
import errand_matcher.helper as helper
import errand_matcher.messages as messages
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

def index(request):
    return render(request, 'errand_matcher/index.html', {'GMAPS_API_KEY': os.environ.get('GMAPS_API_KEY')})

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

def volunteer_signup(request):
    if request.method == 'POST':
        import pdb; pdb.set_trace()
        first_name = request.POST['add-volunteer-first-name']
        last_name = request.POST['add-volunteer-last-name']
        email = request.POST['add-volunteer-email']
        mobile_number = request.POST['add-volunteer-phone']
        frequency = request.POST['frequencyRadio']
        language =  request.POST.getlist('language')
        transportation = request.POST.getlist('transport')
        lat = request.POST['address-latitude']
        lon = request.POST['address-longitude']

        # Check to see if any users already exist with this email as a username
        matches = User.objects.filter(username=email).count()
        if matches > 0:
            return render(request, 'errand_matcher/volunteer-signup-v2.html',
                {'GMAPS_API_KEY': os.environ.get('GMAPS_API_KEY'),
                'base_url': helper.get_base_url(), 'exists': email})

        # Did not find a user, this is fine
        user = User(username=email, 
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=BaseUserManager().make_random_password(),
            user_type=1)
        user.save()

        freq_no = frequency_choice_lookup[frequency]

        walks = False
        has_bike = False
        has_car = False
        if "My own two feet" in transportation:
            walks = True
        if "Bike" in transportation:
            has_bike = True
        if "Car" in transportation:
            has_car = True

        speaks_spanish = False
        speaks_russian = False
        speaks_chinese = False

        if "Spanish" in language:
            speaks_spanish = True
        if "Russian" in language:
            speaks_russian = True
        if "Chinese" in language:
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

        messages.welcome_new_volunteer(volunteer)

        return render(request, 'errand_matcher/volunteer-signup-done.html', {'base_url': helper.get_base_url(), 
            'name': first_name})
    else:
        return render(request, 'errand_matcher/volunteer-signup-v2.html',
            {'GMAPS_API_KEY': os.environ.get('GMAPS_API_KEY'),
            'base_url': helper.get_base_url(),
            'exists': None})

def volunteer_signup_done(request):
    return render(request, 'errand_matcher/volunteer-signup-done.html', {'base_url': helper.get_base_url()})

def requestor(request):
    return render(request, 'errand_matcher/requestor-request.html')

def requestor_login(request):
    if request.method == 'POST':
        mobile_number_str = request.POST.get('phone-input')

        # Is mobile number associated with Requestor?
        requestor = helper.get_user_from_mobile_number_str(mobile_number_str, user_type='requestor')

        # If Volunteer found, create OTP
        if requestor is not None:
            user_otp = UserOTP.objects.create(mobile_number = requestor.mobile_number)

            # deliver OTP
            messages.send_otp(user_otp)
        
            return redirect('requestor_login_otp')
        # If no Requestor found, show warning and redirect back to signup
        else:

            return render(request, 'errand_matcher/requestor-login.html', {
                'warning': "Sorry, we couldn't find a user associated with {}".format(mobile_number_str)})
    else:
        return render(request, 'errand_matcher/requestor-login.html')

def requestor_login_otp(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp-input').strip()
        user_otp = UserOTP.objects.filter(token=otp_input).first()

        # If OTP found, render delivery request page
        if user_otp is not None:
            requestor = Requestor.objects.filter(mobile_number=user_otp.mobile_number).first()
            if requestor is not None:
                return render(request, 'errand_matcher/request-errand.html', {'requestor': requestor})
            # Else warning
            else:
                return render(request, 'errand_matcher/requestor-login-otp.html', {
                    'warning': otp_input})
        
        # If OTP not found, show warning
        else:
            return render(request, 'errand_matcher/requestor-login-otp.html', {
                'warning': otp_input
                })
    else:
        return render(request, 'errand_matcher/requestor-login-otp.html')

def requestor_signup(request):
    if request.method == 'POST':
        import pdb; pdb.set_trace()
        first_name = request.POST['firstname-review']
        last_name = request.POST['lastname-review']
        mobile_number = request.POST['phone-review']
        address = request.POST['address-review']
        apt_no = request.POST['apt-no-review']

        user = User(username=mobile_number, 
            first_name=first_name,
            last_name=last_name,
            email='',
            password=BaseUserManager().make_random_password(),
            user_type=2)
        user.save()

        coord_location = helper.gmaps_geocode(address)

        requestor = Requestor(
            user=user,
            # PhoneNumberField requires country code
            mobile_number='+1' + mobile_number,
            lon=coord_location['lng'],
            lat=coord_location['lat'],
            address_str=address,
            apt_no=apt_no)
        requestor.save()
        return render(request, 'errand_matcher/request-errand.html', 
                {'requestor': requestor, 'requestor_new': True})
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
        volunteer = helper.get_user_from_mobile_number_str(str(volunteer_number))

        # update errand
        errand.status = 2
        errand.claimed_time = timezone.now()
        errand.claimed_volunteer = volunteer
        errand.access_id = uuid.uuid4()
        errand.save()

        messages.confirm_successful_claim(errand, volunteer)

        return HttpResponse(status=204)

    else:
        
        errand = Errand.objects.filter(id=errand_id).first()

        # errand no longer exists
        if errand is None:
            return render(request, 'errand_matcher/errand-DNE.html', {
            'base_url': helper.get_base_url()
            })
        
        # TO DO: verify that volunteer is associated with errand        
        volunteer = helper.get_user_from_mobile_number_str(str(volunteer_number))
        
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

        requestor_number = helper.format_mobile_number(errand.requestor.mobile_number)

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
            'requestor_number': requestor_number,
            'staff_number': staff_number,
            'base_url': helper.get_base_url()
            })

def view_errand(request, errand_id, access_id):
    errand = Errand.objects.filter(access_id=access_id).first()
    errand_expiration_hours = math.floor((errand.due_by - timezone.now()).total_seconds() / 3600)
    requestor_number = helper.format_mobile_number(errand.requestor.mobile_number)
    if errand is not None:
        return render(request, 'errand_matcher/errand-view.html', {
            'access_id': access_id,
            'errand': errand,
            'errand_number': int(errand.id),
            'time_left': errand_expiration_hours,
            'requestor_number': requestor_number,
            'base_url': helper.get_base_url()
            })

    else:
        return render(request, 'errand_matcher/404.html', {'base_url': helper.get_base_url()})

def complete_errand(request, errand_id, access_id):
    if request.method == 'POST':
        errand = Errand.objects.filter(access_id=access_id).first()
        if errand is not None:
            # status = 3 if complete
            errand.status = 3
            errand.completed_time = timezone.now()
            errand.save()

            messages.thank_and_survey(errand.claimed_volunteer)

            errands_completed = len(Errand.objects.filter(claimed_volunteer=errand.claimed_volunteer))
            p = inflect.engine()
            ordinal_errands_completed = p.ordinal(errands_completed)

            return render(request, 'errand_matcher/errand-complete.html', 
                {'errand': errand, 'ordinal_errands_completed': ordinal_errands_completed})
    else:
        return HttpResponseNotAllowed()

def partner(request):
    if request.method == 'POST':
        username = request.POST['partner-login-email']
        password = request.POST['partner-login-password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/partner/dashboard/')
        else:
            return render(request, 'errand_matcher/partner.html', {'warning': 'Your credentials are not correct.'})
    else:
        if request.user.is_authenticated:
            return redirect('/partner/dashboard/')
        else:
            return render(request, 'errand_matcher/partner.html')

def partner_setup(request):
    if request.method == 'POST':
        name = request.POST['setup-name']
        org = request.POST['setup-organization']
        email = request.POST['setup-email']
        phone = request.POST['setup-phone-number']

        content = "We received a request to setup a partner account:\n"\
                "Name: {}\n"\
                "Organization: {}\n"\
                "Email: {}\n"\
                "Phone: {}\n".format(name, org, email, phone)

        message = Mail(
            from_email='team@livelyhood.io',
            to_emails='livelyhood.io@gmail.com',
            subject='LivelyHood Partner Organization Interest',
            html_content=content)
        
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

        return render(request, 'errand_matcher/partner.html', {'setup_done': 'true', 'base_url': helper.get_base_url()})
    else:
        return HttpResponseNotAllowed()

def partner_request(request):
    if request.method == 'POST':
        edit_errand_id = request.POST.get('edit-errand-id')
        if edit_errand_id is None:

            # new request
            requestor_number = request.POST['add-requestor-phone']
            requestor_number_digits = ''.join(i for i in requestor_number if (i.isdigit() or i == '+'))
            requestor_first_name = request.POST['add-requestor-first-name']
            requestor_last_name = request.POST['add-requestor-last-name']
            requestor_address = request.POST['add-requestor-address']
            requestor_apartment = request.POST['add-requestor-apartment']
            requestor_internal_note = request.POST['internal-notes']
            errand_due_by = request.POST['errand-due-by']+" 23:59:59"
            errand_instructions = request.POST['volunteer-instructions']
            coord_location = helper.gmaps_geocode(requestor_address)

            requestor = helper.get_user_from_mobile_number_str(requestor_number_digits, user_type='requestor')

            if len(requestor_number_digits) == 10:
                requestor_number_digits = '+1' + requestor_number_digits

            if requestor is None:
                user = User(
                    username=requestor_number_digits,
                    first_name=requestor_first_name,
                    last_name=requestor_last_name,
                    email='',
                    password=User.objects.make_random_password(),
                    user_type=2)
                user.save()

                requestor = Requestor(
                    user=user,
                    mobile_number=requestor_number_digits,
                    lon=coord_location['lng'],
                    lat=coord_location['lat'],
                    address_str = requestor_address,
                    apt_no = requestor_apartment,
                    internal_note = requestor_internal_note)
                requestor.save()
            else:
                user = requestor.user
                user.first_name = requestor_first_name
                user.last_name = requestor_last_name
                user.save()

                requestor.address_str = requestor_address
                requestor.apt_no = requestor_apartment
                requestor.lon = coord_location['lng']
                requestor.lat = coord_location['lat']
                requestor.internal_note = requestor_internal_note
                requestor.save()

            errand = Errand(
                requested_time = timezone.now(),
                status=0,
                due_by=errand_due_by,
                requestor=requestor,
                additional_info=errand_instructions,
                affiliated_partner=request.user.partner)
            errand.save()
            return redirect('/partner/dashboard/')

        else:

            #edit existing request
            errand_id = request.POST['edit-errand-id']
            requestor_id = request.POST['edit-requestor-id']
            
            requestor_number = request.POST['edit-requestor-phone']
            requestor_number_digits = ''.join(i for i in requestor_number if (i.isdigit() or i == '+'))
            if len(requestor_number_digits) == 10:
                requestor_number_digits = '+1' + requestor_number_digits

            requestor_first_name = request.POST['edit-requestor-first-name']
            requestor_last_name = request.POST['edit-requestor-last-name']
            requestor_address = request.POST['edit-requestor-address']
            requestor_apartment = request.POST['edit-requestor-apartment']
            requestor_internal_note = request.POST['edit-internal-notes']
            errand_due_by = request.POST['edit-errand-due-by'] + " 23:59:59"
            errand_instructions = request.POST['edit-volunteer-instructions']

            user = User.objects.get(id=requestor_id)
            user.username = requestor_number_digits
            user.first_name = requestor_first_name
            user.last_name = requestor_last_name
            user.save()

            requestor = user.requestor
            requestor.mobile_number = requestor_number_digits
            requestor.address_str = requestor_address
            requestor.apt_no = requestor_apartment
            requestor.internal_note = requestor_internal_note
            requestor.save()

            errand = Errand.objects.get(id=errand_id)
            errand.due_by = errand_due_by
            errand.additional_info = errand_instructions
            errand.save()
            return redirect('/partner/dashboard/')
    else:
        return render(request, 'errand_matcher/404.html', {'base_url': helper.get_base_url()})

@csrf_protect
def partner_request_delete(request, errand_id):
    if request.method == 'DELETE':
        errand = Errand.objects.get(id=errand_id)
        errand.delete()
        return HttpResponse(status=200)
    else:
        return HttpResponseNotAllowed()

def partner_password_reset(request):
    if request.method == 'POST':
        recover_email = request.POST['recover-email']
        user = User.objects.filter(username=recover_email).first()
        if user is not None:
            # Generate a password reset token
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            password_reset_token = PasswordResetTokenGenerator().make_token(user)
            password_reset_url = helper.get_base_url() + "/partner/reset/{}/{}".format(uidb64, password_reset_token)

            content = "<p>Hi there, we received a password reset request for your account. Please click here to reset your password:</p>"\
                "<p><a href='{}'>{}</a></p>"\
                "<p>If you did not request a password change, please ignore this message. Thanks,</p>"\
                "<p>Team LivelyHood</p>"\
                "<p>{}</p>".format(password_reset_url, password_reset_url, helper.get_base_url())
            print(content)
            message = Mail(
                from_email='team@livelyhood.io',
                to_emails=recover_email,
                subject='LivelyHood Password Reset',
                html_content=content)
        
            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e.message)
            
        return render(request, 'errand_matcher/partner-password-reset-done.html', {'base_url': helper.get_base_url()})

    else:
        return render(request, 'errand_matcher/partner-password-reset.html', {'base_url': helper.get_base_url()})


def partner_password_reset_done(request):
    return render(request, 'errand_matcher/partner-password-reset-done.html', {'base_url': helper.get_base_url()})

def partner_password_reset_confirm(request, uidb64, token):
    if request.method == 'POST':
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.filter(pk=uid).first()
        password = request.POST['new-password']
        try:
            validate_password(password)
        except:
            return render(request, 'errƒand_matcher/partner-password-reset-confirm.html', 
                {'base_url': helper.get_base_url(), 'warning': 'Your password is not valid.', 'user': user})

        user.set_password(password)
        user.save()
        authenticated_user = authenticate(request, username = user.username, 
                 password = password)
        login(request, authenticated_user)
        return redirect('/partner/dashboard/')

    else:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.filter(pk=uid).first()
        token_generator = PasswordResetTokenGenerator()
        if user is not None and token_generator.check_token(user, token):
            return render(request, 'errand_matcher/partner-password-reset-confirm.html', 
                {'base_url': helper.get_base_url(), 'user': user})
        else:
            return redirect('/error/')

@login_required(login_url='/partner/')
def partner_dashboard(request):
    errands = Errand.objects.filter(affiliated_partner=request.user.partner).order_by('-requested_time')
    if timezone.now().hour < 21: 
        min_date = timezone.now().date() + timedelta(days=1)
    else:
        min_date = timezone.now().date() + timedelta(days=2)
    max_date = timezone.now().date() + timedelta(days=30)

    return render(request, 'errand_matcher/partner-dashboard.html', 
        {'user': request.user,
        'errands': errands,
        'GMAPS_API_KEY': os.environ.get('GMAPS_API_KEY'),
        'min_date': min_date.isoformat(),
        'max_date': max_date.isoformat()})

def partner_signout(request):
    logout(request)
    return redirect('/partner/dashboard/')

