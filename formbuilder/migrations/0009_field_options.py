# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('formbuilder', '0008_auto_20150305_0712'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='options',
            field=django.contrib.postgres.fields.ArrayField(size=None, default=[], base_field=models.CharField(max_length=225), blank=True),
        ),
    ]
