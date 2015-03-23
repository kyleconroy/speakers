# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0043_auto_20150319_0436'),
    ]

    operations = [
        migrations.AddField(
            model_name='call',
            name='application_email',
            field=models.EmailField(max_length=75, blank=True),
            preserve_default=True,
        ),
    ]
