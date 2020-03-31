from django.shortcuts import render
from django.http import HttpResponse
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from errand_matcher.models import ConfirmationToken

def index(request):
    return render(request, 'errand_matcher/index.html')

def begin_signup(request):
    return render(request, 'errand_matcher/begin-signup.html')

def complete_signup(request):
    return render(request, 'errand_matcher/complete-signup.html')

def confirm_email(request):
    if request.method == 'POST':
        current_email = request.POST.get('current-email')
        token = ConfirmationToken()
        print(token)
        token.save()
        url = request.META['HTTP_HOST'] + '/activate/' + str(token.id)
        message = Mail(
            from_email='livelyhood.tech@gmail.com',
            to_emails=current_email,
            subject='Thank you for signing up with Livelyhood!',
            html_content='<a href={}>Activation Link</a>'.format(url))
        # try:
        #     sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        #     response = sg.send(message)
        # except Exception as e:
        #     print(e.message)
    return render(request, 'errand_matcher/email_confirmation.html', {'current_email': current_email})


def activate(request, token_id):
    token = ConfirmationToken.objects.filter(id=token_id).first()
    if token is None:
        token_state = 'Does Not Exist'
    else:
        if token.active:
            token_state = 'Active'
        else:
            token_state = 'Expired'
    return render(request, 'errand_matcher/complete-signup.html', {'token_state': token_state})


def matchable_volunteers(request, requestor_id):
    pass
