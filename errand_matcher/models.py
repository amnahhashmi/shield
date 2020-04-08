from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'volunteer'),
        (2, 'requestor')
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)


# Create your models here.
class Volunteer(models.Model):
    FREQUENCY_CHOICES = (
        (1, 'anytime'),
        (2, '2-3 times per week'),
        (3, 'once a week')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    mobile_number = PhoneNumberField(default='555-555-5555')
    lon = models.FloatField()
    lat = models.FloatField()
    frequency = models.PositiveSmallIntegerField(choices=FREQUENCY_CHOICES)
    walks = models.BooleanField()
    has_bike = models.BooleanField()
    has_car = models.BooleanField()
    speaks_spanish = models.BooleanField()
    speaks_chinese = models.BooleanField()
    speaks_russian = models.BooleanField()
    # Certified that Volunteer has read Health and Safety Protocol
    consented = models.BooleanField()
    opted_out = models.BooleanField(default=False)

class ConfirmationToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(default=True)
    email = models.EmailField(default='livelyhood.tech@gmail.com')

class Requestor(models.Model):

    CONTACT_PREFERENCE_CHOICES = (
        (1, 'sms'),
        (2, 'call')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')
    mobile_number = PhoneNumberField(default='555-555-5555')
    lon = models.FloatField(null=True)
    lat = models.FloatField(null=True)
    contact_preference = models.PositiveSmallIntegerField(choices=CONTACT_PREFERENCE_CHOICES, default=1)

class Errand(models.Model):
    STATUS_CHOICES = (
        (1, 'open'),
        (2, 'in progress'),
        (3, 'complete'),
        (4, 'failed')
    )

    URGENCY_CHOICES = (
        (1, 'less than 24 hours'),
        (2, 'within 3 days')
    )

    REVIEW_CHOICES = (
        (1, 'positive'),
        (2, 'negative')
    )

    requested_time = models.DateTimeField()
    claimed_time = models.DateTimeField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    urgency = models.PositiveSmallIntegerField(choices=URGENCY_CHOICES)
    requestor = models.ForeignKey(Requestor, on_delete=models.CASCADE)
    claimed_volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name='claimed_volunteer', blank=True, null=True)
    contacted_volunteers = models.ManyToManyField(Volunteer, related_name='contacted_volunteers', blank=True)
    requestor_review = models.PositiveSmallIntegerField(choices=REVIEW_CHOICES, blank=True, null=True)
    volunteer_review = models.PositiveSmallIntegerField(choices=REVIEW_CHOICES, blank=True, null=True)

