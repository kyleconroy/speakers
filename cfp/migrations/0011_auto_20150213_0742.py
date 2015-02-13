# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cfp', '0010_auto_20150213_0711'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('first_name', models.CharField(max_length=300)),
                ('last_name', models.CharField(max_length=300)),
                ('email_address', models.EmailField(max_length=254)),
                ('bio', models.TextField(blank=True)),
                ('personal_website', models.URLField(max_length=500, blank=True)),
                ('twitter_handle', models.CharField(max_length=20, blank=True)),
                ('github_handle', models.CharField(max_length=20, blank=True)),
                ('organization', models.CharField(max_length=100, blank=True)),
                ('job_title', models.CharField(max_length=50, blank=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='talk',
            name='profile',
            field=models.ForeignKey(to='cfp.Profile', default=None),
            preserve_default=False,
        ),
    ]
