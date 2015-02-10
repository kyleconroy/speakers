# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0006_auto_20150208_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='tweet_id',
            field=models.BigIntegerField(default=0, db_index=True),
            preserve_default=True,
        ),
    ]
