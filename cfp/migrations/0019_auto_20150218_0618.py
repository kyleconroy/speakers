# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0018_auto_20150216_0458'),
    ]

    operations = [
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('conference', models.ForeignKey(to='cfp.Conference')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='talk',
            name='format',
            field=models.ForeignKey(blank=True, null=True, to='cfp.Format'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, help_text='Your number is private and never shared with conferences'),
            preserve_default=True,
        ),
    ]
