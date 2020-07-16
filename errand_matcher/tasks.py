from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger
import errand_matcher.helper as helper
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

weekday_lookup = {
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
    6: 'Saturday',
    7: 'Sunday'
}

url_lookup = {
    'LOCAL': 'http://127.0.0.1:8000',
    'STAGING': 'https://staging-shieldcovid.herokuapp.com',
    'PROD': 'https://www.livelyhood.io'
}

@shared_task
def match_errands():
    logger.info('Matching errands')
    errands = Errand.objects.filter(status=1)
    for errand in errands:

        # convert to failed status if exceeded 1 day since creation
        # for urgent or 3 days for non-urgent
        days_to_add = 1 if errand.urgency == 1 else 3
        errand_expiration = errand.requested_time + timedelta(days=days_to_add)
        if timezone.now() > errand_expiration:
            errand.status = 4
            errand.save()

            # alert on-call staffer
            site_configuration = SiteConfiguration.objects.first()
            message = 'ERRAND FAILURE! {} {}: {} requested at {}'.format(
                errand.requestor.user.first_name, 
                errand.requestor.user.last_name,
                helper.strip_mobile_number(errand.requestor.mobile_number),
                errand.requested_time)
 
            helper.send_sms(
                helper.format_number(site_configuration.mobile_number_on_call), 
                message)

        else:
            if errand.request_round < 10:
                # TO DO: what if there are no volunteers?
                volunteers = helper.match_errand_to_volunteers(errand)
                deadline_str = '{} at 6 p.m.'.format(
                    weekday_lookup[(timezone.now() + timedelta(days=days_to_add)).date().isoweekday()])

                deploy_stage = os.environ.get('DEPLOY_STAGE')
                url_base = url_lookup[deploy_stage]

                for v in volunteers:
                    if v.mobile_number == '':
                        continue
                    else:
                        url = "{}/errand/{}/accept/{}".format(
                            url_base, 
                            errand.id, 
                            helper.strip_mobile_number(v.mobile_number))

                        message = "LivelyHood here! {} needs help getting groceries! Can you make a delivery by {}?"\
                        " Click here for more information and to let us know if you can help. {}".format(
                            errand.requestor.user.first_name, deadline_str, url)
                        
                        helper.send_sms(helper.format_mobile_number(v.mobile_number), message)
                        errand.contacted_volunteers.add(v)

                errand.request_round +=1
                errand.save()

TWILIO_FLOWS = {
    'Req_Happy_VolDelivered': 'FW554a336fe5d6c246d934a9e77e6dadb6',
}

@shared_task
def cleanup_tokens():
    # expire tokens after 10 minutes
    ten_minutes_ago = timezone.now() - timedelta(minutes=15)
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
