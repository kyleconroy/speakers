# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0030_auto_20150228_0435'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conference',
            name='programming_language',
        ),
    ]
