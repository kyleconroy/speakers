# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0039_profile_photo_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('cfp_url', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
