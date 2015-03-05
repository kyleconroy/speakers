# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cfp', '0033_auto_20150301_0150'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='watchers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='conference',
            name='topics',
            field=models.ManyToManyField(to='cfp.Topic', blank=True),
            preserve_default=True,
        ),
    ]
