from __future__ import absolute_import, unicode_literals

from celery import shared_task
from errand_matcher.models import User, Volunteer


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
