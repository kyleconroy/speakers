# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0037_auto_20150308_0822'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='linkedin',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='speaking_experience',
            field=models.TextField(help_text='Please include links to videos of you speaking', blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='usermailing',
            unique_together=set([('owner', 'call')]),
        ),
    ]
