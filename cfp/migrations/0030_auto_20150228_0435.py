# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0029_auto_20150228_0428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='value',
            field=models.CharField(max_length=100, unique=True),
            preserve_default=True,
        ),
    ]
