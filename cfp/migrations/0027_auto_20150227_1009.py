# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0026_auto_20150227_0848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='format',
            name='conference',
        ),
        migrations.RemoveField(
            model_name='track',
            name='conference',
        ),
        migrations.RemoveField(
            model_name='call',
            name='needs_audience',
        ),
        migrations.RemoveField(
            model_name='talk',
            name='abstract',
        ),
        migrations.RemoveField(
            model_name='talk',
            name='audience',
        ),
        migrations.RemoveField(
            model_name='talk',
            name='format',
        ),
        migrations.DeleteModel(
            name='Format',
        ),
        migrations.RemoveField(
            model_name='talk',
            name='track',
        ),
        migrations.DeleteModel(
            name='Track',
        ),
    ]
