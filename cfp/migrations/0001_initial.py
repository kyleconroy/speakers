# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('notify', models.DateField(blank=True)),
                ('lanyrd_url', models.URLField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('slug', models.CharField(max_length=45, db_index=True)),
                ('name', models.CharField(max_length=45)),
                ('venue', models.CharField(max_length=100, blank=True)),
                ('city', models.CharField(max_length=100)),
                ('country', django_countries.fields.CountryField(default='US', max_length=2)),
                ('state', models.CharField(max_length=100, blank=True)),
                ('tagline', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('twitter_handle', models.CharField(max_length=15, blank=True)),
                ('twitter_hashtag', models.CharField(max_length=20, blank=True)),
                ('start', models.DateField(db_index=True)),
                ('end', models.DateField(db_index=True)),
                ('maps_url', models.URLField(max_length=300, blank=True)),
                ('website_url', models.URLField()),
                ('conduct_url', models.URLField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='call',
            name='conference',
            field=models.ForeignKey(to='cfp.Conference'),
            preserve_default=True,
        ),
    ]
