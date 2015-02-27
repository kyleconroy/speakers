# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('value', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('required', models.BooleanField(default=False)),
                ('label', models.CharField(default='', max_length=255)),
                ('initial', models.CharField(default='', max_length=255)),
                ('kind', models.SmallIntegerField(choices=[(1, 'BooleanField'), (2, 'CharField'), (3, 'ChoiceField'), (4, 'TypedChoiceField'), (5, 'DateField'), (6, 'DateTimeField'), (7, 'DecimalField'), (8, 'EmailField'), (9, 'FileField'), (10, 'FilePathField'), (11, 'FloatField'), (12, 'ImageField'), (13, 'IntegerField'), (14, 'IPAddressField'), (15, 'GenericIPAddressField'), (16, 'MultipleChoiceField'), (17, 'TypedChoiceField'), (18, 'NullBooleanField'), (19, 'RegexField'), (20, 'SlugField'), (21, 'TimeField'), (22, 'URLField')], default=2)),
                ('help_text', models.CharField(default='', max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('form', models.ForeignKey(to='formbuilder.Form')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='field',
            name='form',
            field=models.ForeignKey(to='formbuilder.Form'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entry',
            name='field',
            field=models.ForeignKey(to='formbuilder.Field'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entry',
            name='submission',
            field=models.ForeignKey(to='formbuilder.Submission'),
            preserve_default=True,
        ),
    ]
