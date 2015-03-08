# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cfp', '0034_auto_20150305_0621'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('q', models.CharField(max_length=254, blank=True, default='')),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, default='')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('topic', models.ForeignKey(blank=True, to='cfp.Topic', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='call',
            name='end',
            field=models.DateField(help_text='Dates are formated using MM/DD/YYYY', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='call',
            name='start',
            field=models.DateField(help_text='Dates are formated using MM/DD/YYYY', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='conference',
            name='end',
            field=models.DateField(help_text='Dates are formated using MM/DD/YYYY', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='conference',
            name='start',
            field=models.DateField(help_text='Dates are formated using MM/DD/YYYY', db_index=True),
            preserve_default=True,
        ),
    ]
