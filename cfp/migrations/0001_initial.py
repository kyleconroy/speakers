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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('slug', models.CharField(db_index=True, max_length=45)),
                ('name', models.CharField(max_length=45)),
                ('venue', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('state', models.CharField(max_length=100)),
                ('tagline', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('twitter_handle', models.CharField(blank=True, max_length=15)),
                ('twitter_hashtag', models.CharField(blank=True, max_length=20)),
                ('start', models.DateField(db_index=True)),
                ('end', models.DateField(db_index=True)),
                ('maps_url', models.URLField(blank=True, max_length=300)),
                ('website_url', models.URLField()),
                ('conduct_url', models.URLField(blank=True)),
                ('call', models.ForeignKey(to='cfp.Call')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
