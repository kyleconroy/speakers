# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0008_auto_20150211_0407'),
    ]

    operations = [
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=300)),
                ('abstract', models.TextField()),
                ('audience', models.IntegerField(default=0, choices=[('0', 'None'), ('1', 'Beginner'), ('2', 'Intermidiate'), ('3', 'Advancded')])),
                ('track', models.ForeignKey(to='cfp.Talk')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('conference', models.ForeignKey(to='cfp.Conference')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
