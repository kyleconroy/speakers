# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0014_talk_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talk',
            name='token',
            field=models.CharField(unique=True, max_length=15),
            preserve_default=True,
        ),
    ]
