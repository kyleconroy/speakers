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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('start', models.DateField(db_index=True)),
                ('end', models.DateField(db_index=True)),
                ('notify', models.DateField()),
                ('lanyrd_url', models.URLField(blank=True, max_length=500)),
                ('application_url', models.URLField(blank=True, max_length=1000)),
                ('approved', models.BooleanField(default=False, db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('slug', models.CharField(db_index=True, max_length=100)),
                ('legacy_slug', models.CharField(db_index=True, max_length=100)),
                ('name', models.CharField(max_length=200)),
                ('venue', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('country', django_countries.fields.CountryField(default='US', max_length=2)),
                ('state', models.CharField(blank=True, max_length=100)),
                ('tagline', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('twitter_handle', models.CharField(blank=True, max_length=20)),
                ('twitter_hashtag', models.CharField(blank=True, max_length=20)),
                ('start', models.DateField(db_index=True)),
                ('end', models.DateField(db_index=True)),
                ('maps_url', models.URLField(blank=True, max_length=1000)),
                ('website_url', models.URLField(max_length=500)),
                ('conduct_url', models.URLField(blank=True, max_length=500)),
            ],
            options={
                'ordering': ['slug', 'start'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='conference',
            unique_together=set([('slug', 'start')]),
        ),
        migrations.AddField(
            model_name='call',
            name='conference',
            field=models.ForeignKey(to='cfp.Conference'),
            preserve_default=True,
        ),
    ]
