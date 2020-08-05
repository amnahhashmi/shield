from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger
import errand_matcher.helper as helper
import errand_matcher.messages as messages
from errand_matcher.models import Errand
from errand_matcher.models import SiteConfiguration
from errand_matcher.models import UserOTP
import os
from datetime import timedelta
from datetime import datetime
from datetime import date
import phonenumbers
from django.utils import timezone

logger = get_task_logger(__name__)

@shared_task
def match_errands():
    logger.info('Matching errands')
    errands = Errand.objects.filter(status=1)
    for errand in errands:
        # convert to failed status if past due
        if timezone.now() > errand.due_by:
            errand.status = 4
            errand.save()

        # alert on-call staffer if errand still unclaimed after last round
        if errand.request_round == helper.get_max_request_rounds():
            messages.alert_staff_of_unclaimed_errand(errand)
            continue

        # TO DO: what if there are no volunteers?
        volunteers = helper.match_errand_to_volunteers(errand)
        for volunteer in volunteers:
            messages.alert_volunteer_to_claim_errand(errand, volunteer)
            errand.contacted_volunteers.add(volunteer)
        
        errand.request_round +=1
        errand.save()

TWILIO_FLOWS = {
    'Req_Happy_VolDelivered': 'FW554a336fe5d6c246d934a9e77e6dadb6',
}

@shared_task
def cleanup_tokens():
    # expire tokens after 10 minutes
    ten_minutes_ago = timezone.now() - timedelta(minutes=10)
    tokens_older_than_ten_mins = UserOTP.objects.filter(created_at__lte=ten_minutes_ago)
    tokens_older_than_ten_mins.delete()

@shared_task
def send_errand_completion_messages():
    # for errands 1 day ago
    twenty_four_hour_errands = Errand.objects.filter(status=2, urgency=1, 
        claimed_time__gte=timezone.now()+timedelta(days=-1))
    three_day_errands = Errand.objects.filter(status=2, urgency=2,
        claimed_time__gte=timezone.now()+timedelta(days=-3))
    for errand in list(twenty_four_hour_errands) + list(three_day_errands):
        execution = twilio_client.studio \
            .v1 \
            .flows(settings.TWILIO_FLOWS['Req_Happy_VolDelivered']) \
            .executions \
            .create(to=requestor.mobile_number.as_e164, from_=settings.TWILIO_NUMBER)
        errand.status=3
        errand.save()
