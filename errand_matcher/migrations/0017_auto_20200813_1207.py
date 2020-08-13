# Generated by Django 3.0.4 on 2020-08-13 16:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('errand_matcher', '0016_auto_20200805_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='mobile_number',
            field=phonenumber_field.modelfields.PhoneNumberField(default='555-555-5555', max_length=128, region=None),
        ),
        migrations.AlterField(
            model_name='errand',
            name='due_by',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 13, 16, 7, 14, 62849, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userotp',
            name='token',
            field=models.CharField(default='182224', max_length=6),
        ),
    ]
