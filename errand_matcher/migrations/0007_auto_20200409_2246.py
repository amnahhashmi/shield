# Generated by Django 3.0.4 on 2020-04-09 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('errand_matcher', '0006_errand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='errand',
            name='requestor_review',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'positive'), (2, 'negative')], null=True),
        ),
        migrations.AlterField(
            model_name='errand',
            name='volunteer_review',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'positive'), (2, 'negative')], null=True),
        ),
    ]
