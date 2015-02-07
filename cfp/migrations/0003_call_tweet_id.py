# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0002_auto_20150206_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='call',
            name='tweet_id',
            field=models.IntegerField(db_index=True, default=0),
            preserve_default=False,
        ),
    ]
