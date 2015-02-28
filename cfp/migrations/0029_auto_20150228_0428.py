# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.db import transaction


@transaction.atomic
def create_topics(apps, schema_editor):
    Topic = apps.get_model("cfp", "Topic")
    Conference = apps.get_model("cfp", "Conference")

    for conf in Conference.objects.exclude(programming_language=''):
        topic = Topic.object.get_or_create(value=conf.programming_language)
        conf.topics.add(topic)


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0028_auto_20150228_0428'),
    ]

    operations = [
        migrations.RunPython(create_topics)
    ]
