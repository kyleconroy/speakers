# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0009_talk_track'),
    ]

    operations = [
        migrations.AddField(
            model_name='call',
            name='needs_audience',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='talk',
            name='call',
            field=models.ForeignKey(default=None, to='cfp.Call'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='talk',
            name='state',
            field=django_fsm.FSMField(default='new', protected=True, max_length=50, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='talk',
            name='audience',
            field=models.IntegerField(default=1, choices=[('1', 'Beginner'), ('2', 'Intermidiate'), ('3', 'Advancded')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='talk',
            name='track',
            field=models.ForeignKey(null=True, blank=True, to='cfp.Talk'),
            preserve_default=True,
        ),
    ]
