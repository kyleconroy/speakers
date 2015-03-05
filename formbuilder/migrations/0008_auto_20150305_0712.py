# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('formbuilder', '0007_auto_20150227_0848'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='created',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2015, 3, 5, 7, 12, 6, 280002, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='field',
            name='widget',
            field=models.SmallIntegerField(blank=True, choices=[(0, 'Default widget'), (1, 'Textarea'), (2, 'NumberInput'), (3, 'EmailInput'), (4, 'URLInput'), (5, 'HiddenInput'), (6, 'DateInput'), (7, 'DateTimeInput'), (8, 'TimeInput'), (9, 'RadioSelect'), (10, 'CheckboxSelectMultiple')], default=0),
            preserve_default=True,
        ),
    ]
