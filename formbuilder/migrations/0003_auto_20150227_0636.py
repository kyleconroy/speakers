# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formbuilder', '0002_auto_20150227_0607'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='name',
            field=models.CharField(max_length=255, default='name'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='field',
            unique_together=set([('form', 'name')]),
        ),
    ]
