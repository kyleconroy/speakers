# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0045_auto_20150401_0530'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=[], blank=True, size=None),
        ),
        migrations.AddField(
            model_name='savedsearch',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=[], blank=True, size=None),
        ),
        migrations.AlterField(
            model_name='call',
            name='application_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='interest',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='usermailing',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
