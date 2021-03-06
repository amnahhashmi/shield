# Generated by Django 3.0.4 on 2020-08-13 22:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
from errand_matcher import helper


# previous migration 13 failed because apt no was required
def add_address_str_to_requestor(apps, schema_editor):
    Requestor = apps.get_model('errand_matcher', 'Requestor')
    for r in Requestor.objects.all():
        address = helper.gmaps_reverse_geocode((r.lat, r.lon))
        r.address_str = address
        r.save()


class Migration(migrations.Migration):

    dependencies = [
        ('errand_matcher', '0017_auto_20200813_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='errand',
            name='due_by',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 13, 22, 3, 50, 902402, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='requestor',
            name='apt_no',
            field=models.CharField(blank=True, default='', max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='userotp',
            name='token',
            field=models.CharField(default='807238', max_length=6),
        ),
        migrations.RunPython(add_address_str_to_requestor)
    ]
