# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cfp', '0035_auto_20150308_0508'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMailing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(max_length=75)),
                ('subject', models.CharField(max_length=500)),
                ('text', models.TextField()),
                ('html', models.TextField()),
                ('call', models.ForeignKey(to='cfp.Call')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
