# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0003_call_approved'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conference',
            options={'ordering': ['slug', 'start']},
        ),
        migrations.AlterField(
            model_name='call',
            name='approved',
            field=models.BooleanField(db_index=True, default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='call',
            name='end',
            field=models.DateField(db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='call',
            name='notify',
            field=models.DateField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='call',
            name='start',
            field=models.DateField(db_index=True),
            preserve_default=True,
        ),
    ]
