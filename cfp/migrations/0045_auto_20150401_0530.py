# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0044_call_application_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestion',
            name='state',
            field=django_fsm.FSMField(max_length=50, db_index=True, protected=True, default='inbox'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='suggestion',
            name='cfp_url',
            field=models.URLField(max_length=1000),
            preserve_default=True,
        ),
    ]
