# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def combine_names(apps, schema_editor):
    Profile = apps.get_model("cfp", "Profile")
    for profile in Profile.objects.all():
        profile.name = "%s %s" % (profile.first_name, profile.last_name)
        profile.save()


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0021_profile_name'),
    ]

    operations = [
        migrations.RunPython(combine_names),
    ]
