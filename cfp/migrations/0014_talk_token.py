# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0013_auto_20150213_0805'),
    ]

    operations = [
        migrations.AddField(
            model_name='talk',
            name='token',
            field=models.CharField(default='foo', max_length=15),
            preserve_default=False,
        ),
    ]
