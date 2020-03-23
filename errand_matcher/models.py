from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'volunteer'),
        (2, 'requestor')
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)


# Create your models here.
class Volunteer(models.Model):
    FREQUENCY_CHOICES = (
        (1, 'anytime'),
        (2, '2-3 times per week'),
        (3, 'once a week')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
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

