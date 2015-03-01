# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0032_topic_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='created',
            field=models.DateTimeField(db_index=True, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='conference',
            name='country',
            field=django_countries.fields.CountryField(db_index=True, max_length=2, default='US'),
            preserve_default=True,
        ),
    ]
