# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0011_auto_20150213_0742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='talk',
            name='audience',
            field=models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermidiate'), (3, 'Advancded')], blank=True),
            preserve_default=True,
        ),
    ]
