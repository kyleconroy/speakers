# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0002_auto_20150201_0634'),
    ]

    operations = [
        migrations.AddField(
            model_name='call',
            name='approved',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
