from __future__ import absolute_import, unicode_literals

from celery import shared_task
import errand_matcher.helper as helper
from errand_matcher.models import Errand
import os
from datetime import timedelta
from datetime import date
import phonenumbers
from django.utils import timezone

@shared_task
def match_errands():
	errands = Errand.objects.filter(status=1)
	for errand in errands:
		# TO DO: notify of failure state
		if errand.requestor_round == 2:
			errand.status = 4
			errand.save()
			continue

		# TO DO: what if there are no volunteers?
        volunteers = helper.match_errand_to_volunteers(errand)

        days_to_add = 1 if errand.urgency == 1 else 3

        deadline_str = '{} at 6 p.m.'.format(
            weekday_lookup[(timezone.now() + timedelta(days=1)).date().isoweekday()])

        requestor_number = errand.requestor.mobile_number
        requestor_number_str= phonenumbers.format_number(requestor_number, 
        	phonenumbers.PhoneNumberFormat.E164)
        requestor_number_stripped = requestor_number.replace('+1', '')

        if os.environ.get('LOCAL'):
            url_base = "http://127.0.0.1/"
        else:
            url_base = "https://www.livelyhood.io"
        
        url = "{}/errand/{}/accept/{}".format(url_base,
                errand.id, requestor_number_stripped)
        tiny_url = helper.make_tiny_url(url)

        # TO DO: what if no volunteers?
        for v in volunteers:
            message = "{} needs help getting groceries! Can you make a delivery by {}?"\
            " Only accept if you're sure that you can make it,"\
            " since {} relies on LivelyHood to receive her living essentials. Accept request at {}".format(
                errand.requestor.user.first_name, deadline_str, errand.requestor.user.first_name, url)
            v_number = phonenumbers.format_number(
                v.mobile_number, phonenumbers.PhoneNumberFormat.NATIONAL)
            send_sms(v_number, message)
            errand.contacted_volunteers.add(v)

        errand.request_round +=1
        errand.save()

TWILIO_FLOWS = {
    'Req_Happy_VolDelivered': 'FW554a336fe5d6c246d934a9e77e6dadb6',
}

@shared_task
def send_errand_completion_messages():
	# for errands 1 day ago
    24_hour_errands = Errand.objects.filter(status=2, urgency=1, 
    	claimed_time__gte=timezone.now()+timedelta(days=-1))
    3_day_errands = Errand.objects.filter(status=2, urgency=2,
    	claimed_time__gte=timezone.now()+timedelta(days=-3))
    for errand in list(24_hour_errands) + list(3_day_errands):
        execution = twilio_client.studio \
            .v1 \
            .flows(settings.TWILIO_FLOWS['Req_Happy_VolDelivered']) \
            .executions \
            .create(to=requestor.mobile_number.as_e164, from_=settings.TWILIO_NUMBER)
        errand.status=3
        errand.save()
