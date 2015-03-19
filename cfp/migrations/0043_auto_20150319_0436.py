# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0042_conference_organizer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='github_handle',
            field=models.CharField(max_length=45, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='twitter_handle',
            field=models.CharField(max_length=45, blank=True),
            preserve_default=True,
        ),
    ]
