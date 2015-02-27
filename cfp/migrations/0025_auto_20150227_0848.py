# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formbuilder', '0007_auto_20150227_0848'),
        ('cfp', '0024_auto_20150221_0555'),
    ]

    operations = [
        migrations.AddField(
            model_name='call',
            name='form',
            field=models.ForeignKey(to='formbuilder.Form', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='talk',
            name='submission',
            field=models.ForeignKey(to='formbuilder.Submission', null=True),
            preserve_default=True,
        ),
    ]
