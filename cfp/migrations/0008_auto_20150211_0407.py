# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0007_auto_20150210_0452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='legacy_slug',
            field=models.CharField(db_index=True, max_length=100, blank=True),
            preserve_default=True,
        ),
    ]
