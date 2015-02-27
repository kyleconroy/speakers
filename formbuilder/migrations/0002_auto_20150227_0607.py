# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formbuilder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='name',
            field=models.CharField(default='Name', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='field',
            name='help_text',
            field=models.CharField(blank=True, default='', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='field',
            name='initial',
            field=models.CharField(blank=True, default='', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='field',
            name='kind',
            field=models.SmallIntegerField(choices=[(1, 'BooleanField'), (2, 'CharField'), (3, 'ChoiceField'), (4, 'TypedChoiceField'), (5, 'DateField'), (6, 'DateTimeField'), (7, 'DecimalField'), (8, 'EmailField'), (9, 'FileField'), (10, 'FilePathField'), (11, 'FloatField'), (12, 'ImageField'), (13, 'IntegerField'), (14, 'IPAddressField'), (15, 'GenericIPAddressField'), (16, 'MultipleChoiceField'), (17, 'TypedChoiceField'), (18, 'NullBooleanField'), (19, 'RegexField'), (20, 'SlugField'), (21, 'TimeField'), (22, 'URLField')], blank=True, default=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='field',
            name='label',
            field=models.CharField(blank=True, default='', max_length=255),
            preserve_default=True,
        ),
    ]
