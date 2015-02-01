# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='conference',
            unique_together=set([('slug', 'start')]),
        ),
    ]
