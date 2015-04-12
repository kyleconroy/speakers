# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formbuilder', '0010_auto_20150412_0823'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='option',
            name='field',
        ),
        migrations.DeleteModel(
            name='Option',
        ),
    ]
