# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0003_call_tweet_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='call',
            name='approved',
        ),
        migrations.AddField(
            model_name='call',
            name='state',
            field=django_fsm.FSMField(db_index=True, default='new', max_length=50, protected=True),
            preserve_default=True,
        ),
    ]
