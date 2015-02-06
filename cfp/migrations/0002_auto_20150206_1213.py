# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conference',
            old_name='venue',
            new_name='venue_name',
        ),
        migrations.AddField(
            model_name='call',
            name='description',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conference',
            name='lanyrd_url',
            field=models.URLField(max_length=500, blank=True, unique=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conference',
            name='venue_address',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='call',
            name='lanyrd_url',
            field=models.URLField(max_length=500, blank=True, unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='conference',
            name='description',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
