# Generated by Django 3.0.4 on 2020-07-17 00:34

from django.db import migrations, models
from errand_matcher import helper

def add_address_str_to_requestor(apps, schema_editor):
    Requestor = apps.get_model('errand_matcher', 'Requestor')
    for r in Requestor.objects.all():
        address = helper.gmaps_reverse_geocode((r.lat, r.lon))
        r.address_str = address
        r.save()

class Migration(migrations.Migration):

    dependencies = [
        ('errand_matcher', '0012_auto_20200717_0028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='volunteer',
            name='address_str',
        ),
        migrations.RemoveField(
            model_name='volunteer',
            name='apt_no',
        ),
        migrations.AddField(
            model_name='requestor',
            name='address_str',
            field=models.CharField(default='', max_length=1024),
        ),
        migrations.AddField(
            model_name='requestor',
            name='apt_no',
            field=models.CharField(default='', max_length=8),
        ),
        migrations.AlterField(
            model_name='userotp',
            name='token',
            field=models.CharField(default='098823', max_length=6),
        ),
        migrations.RunPython(add_address_str_to_requestor)
    ]
