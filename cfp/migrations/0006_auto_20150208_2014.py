# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0005_auto_20150208_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='description',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='conference',
            name='lanyrd_url',
            field=models.URLField(max_length=500, blank=True),
            preserve_default=True,
        ),
    ]
