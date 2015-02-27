# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formbuilder', '0004_option'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='order',
            field=models.SmallIntegerField(blank=True, default=0),
            preserve_default=True,
        ),
    ]
