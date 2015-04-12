# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def add_tags(apps, schema_editor):
    Conference = apps.get_model("cfp", "Conference")
    for conf in Conference.objects.all():
        conf.tags = [t.value for t in conf.topics.all()]
        conf.save()

    SavedSearch = apps.get_model("cfp", "SavedSearch")
    for search in SavedSearch.objects.all():
        if search.topic:
            search.tags = [search.topic.value]
            search.save()


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0046_auto_20150412_0646'),
    ]

    operations = [
        migrations.RunPython(add_tags),
    ]
