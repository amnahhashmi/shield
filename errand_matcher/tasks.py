from __future__ import absolute_import, unicode_literals

from celery import shared_task
from errand_matcher.models import User


@shared_task
def add(x, y):
    return x + y

@shared_task
def count_users():
    return User.objects.count()
