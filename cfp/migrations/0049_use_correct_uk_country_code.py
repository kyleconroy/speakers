# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def fix_conference_country_code(apps, schema_editor):
    Conference = apps.get_model("cfp", "Conference")

    for conference in Conference.objects.all():
        if conference.country == "UK":
            conference.country = "GB"
            conference.save()

class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0048_auto_20150412_0740'),
    ]

    operations = [
        migrations.RunPython(fix_conference_country_code)
    ]
