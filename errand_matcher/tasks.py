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
    errands = Errand.objects.filter(status=1)
    for errand in errands:
        # convert to failed status if past due
        if timezone.now() > errand.due_by:
            errand.status = 4
            errand.save()

        # alert on-call staffer if errand still unclaimed after last round
        if errand.request_round >= helper.get_max_request_rounds():
            messages.alert_staff_of_unclaimed_errand(errand)
            continue

        # TO DO: what if there are no volunteers?
        volunteers = helper.match_errand_to_volunteers(errand)
        for volunteer in volunteers:
            messages.alert_volunteer_to_claim_errand(errand, volunteer)
            errand.contacted_volunteers.add(volunteer)
        
        errand.request_round +=1
        errand.save()


@shared_task
def activate_errands():
    errands = Errand.objects.filter(status=0)
    for errand in errands:
        # convert to open status if within 5 days of due by
        if timezone.now() > errand.due_by + timedelta(days=-5):
            errand.status = 1
            errand.save()


@shared_task
def complete_errands():
    # ask volunteer to mark in-progress errand (status=2) as done 1 day after due
    errands = Errand.objects.filter(status=2)
    for errand in errands:
        if timezone.now() > errand.due_by:
            messages.remind_volunteer_to_complete(errand, errand.claimed_volunteer)


@shared_task
def cleanup_tokens():
    # expire tokens after 10 minutes
    ten_minutes_ago = timezone.now() - timedelta(minutes=10)
    tokens_older_than_ten_mins = UserOTP.objects.filter(created_at__lte=ten_minutes_ago)
    tokens_older_than_ten_mins.delete()

