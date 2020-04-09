from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import ensure_csrf_cookie
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from errand_matcher.models import ConfirmationToken, User, Volunteer

frequency_choice_lookup = {
    'Anytime': 1,
    '2-3 times a week': 2,
    'Once a week': 3
}

def index(request):
    return render(request, 'errand_matcher/index.html')

def begin_signup(request):
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
            mobile_number=mobile_number,
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
        return HttpResponse(status=204)
    else:
        return render(request, 'errand_matcher/begin-signup.html')

def confirm_email(request):
    if request.method == 'POST':
        current_email = request.POST.get('current-email')
        # AH 4.16.20: to reduce signup friction, removing activation email
        # token = ConfirmationToken(email=current_email)
        # token.save()
        # url = request.META['HTTP_HOST'] + '/activate/' + str(token.id)
        # message = Mail(
        #     from_email='livelyhood.tech@gmail.com',
        #     to_emails=current_email,
        #     subject='Welcome to Livelyhood',
        #     html_content='Follow the link to finish activating your account')
        # message.template_id = 'd-b0b0a7af49f24ca38b29c125384abba8'
        # message.dynamic_template_data = {
        #     'volunteerURL': url
        # }
        # try:
        #     sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        #     response = sg.send(message)
        # except Exception as e:
        #     print(e.message)
    # return render(request, 'errand_matcher/email-confirmation-end.html', {'current_email': current_email})
        return render(request, 'errand_matcher/complete-signup.html',
         {'token_state': 'Active', 'email': current_email})
    else:
        return HttpResponseNotAllowed(('POST',))

@ensure_csrf_cookie
def activate(request, token_id):
    token = ConfirmationToken.objects.filter(id=token_id).first()
    if token is None:
        token_state = 'Does Not Exist'
    else:
        if token.active:
            token_state = 'Active'
        else:
            token_state = 'Expired'
    return render(request, 'errand_matcher/complete-signup.html', {'token_state': token_state, 'email': token.email})

def requestor_signup(request):
    return render(request, 'errand_matcher/requestor-signup.html')

def matchable_volunteers(request, requestor_id):
    pass

def health_and_safety(request):
    return render(request, 'errand_matcher/health-and-safety.html')
