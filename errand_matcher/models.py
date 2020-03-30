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

class Requestor(models.Model):
    pass

