# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formbuilder', '0003_auto_20150227_0636'),
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('field', models.ForeignKey(to='formbuilder.Field')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
