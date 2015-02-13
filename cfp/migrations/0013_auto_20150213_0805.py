# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0012_auto_20150213_0755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talk',
            name='track',
            field=models.ForeignKey(to='cfp.Track', blank=True, null=True),
            preserve_default=True,
        ),
    ]
