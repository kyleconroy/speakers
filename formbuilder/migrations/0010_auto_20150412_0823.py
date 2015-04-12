# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

def add_options(apps, schema_editor):
    Field = apps.get_model("formbuilder", "Field")
    for field in Field.objects.all():
        field.options = [o.value for o in field.option_set.all()]
        field.save()


class Migration(migrations.Migration):

    dependencies = [
        ('formbuilder', '0009_field_options'),
    ]

    operations = [
        migrations.RunPython(add_options),
    ]
