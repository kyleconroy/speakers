# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0019_auto_20150218_0618'),
    ]

    operations = [
        migrations.AddField(
            model_name='call',
            name='hosted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20),
            preserve_default=True,
        ),
    ]
