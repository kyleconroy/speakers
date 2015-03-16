# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0041_interest'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='organizer',
            field=models.EmailField(blank=True, max_length=254),
            preserve_default=True,
        ),
    ]
