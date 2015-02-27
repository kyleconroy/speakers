# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formbuilder', '0005_field_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='widget',
            field=models.SmallIntegerField(choices=[(0, 'Default widget'), (1, 'TextArea'), (2, 'NumberInput'), (3, 'EmailInput'), (4, 'URLInput'), (5, 'HiddenInput'), (6, 'DateInput'), (7, 'DateTimeInput'), (8, 'TimeInput')], blank=True, default=0),
            preserve_default=True,
        ),
    ]
