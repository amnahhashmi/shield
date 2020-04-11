from __future__ import absolute_import, unicode_literals

from django.conf import settings
from celery import shared_task
from errand_matcher.models import Errand, Requestor, User, Volunteer
from twilio.rest import Client


twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

@shared_task
def add(x, y):
    return x + y

@shared_task
def count_users():
    return User.objects.count()

@shared_task
def match_errands():
    count = Volunteer.objects.count()
    print(count)

@shared_task
def send_errand_completion_messages():
    # TODO: Handle 1 vs 3 day flow
    errands = Errand.objects.filter(status=3, requestor_confirmed__isnull=True)
    for errand in errands:
        requestor = Requestor.objects.get(user_id=errand.requestor_id)
        execution = twilio_client.studio \
            .v1 \
            .flows(settings.TWILIO_FLOWS['Req_Happy_VolDelivered']) \
            .executions \
            .create(to=requestor.mobile_number.as_e164, from_=settings.TWILIO_NUMBER)
        errand.requestor_confirmed=False
        errand.save()
