# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0047_auto_20150412_0647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conference',
            name='topics',
        ),
        migrations.RemoveField(
            model_name='savedsearch',
            name='topic',
        ),
    ]
