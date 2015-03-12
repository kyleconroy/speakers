# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0038_auto_20150312_0320'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='photo_url',
            field=models.URLField(max_length=500, help_text='Bigger than 500x500 preferred', blank=True),
            preserve_default=True,
        ),
    ]
