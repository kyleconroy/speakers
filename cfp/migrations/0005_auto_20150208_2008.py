# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0004_auto_20150207_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='lanyrd_url',
            field=models.URLField(blank=True, max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='call',
            name='notify',
            field=models.DateField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='call',
            name='tweet_id',
            field=models.IntegerField(db_index=True, default=0),
            preserve_default=True,
        ),
    ]
