# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.db import transaction


@transaction.atomic
def create_forms_and_submissions(apps, schema_editor):
    Call = apps.get_model("cfp", "Call")
    Form = apps.get_model("formbuilder", "Form")

    for call in Call.objects.filter(state='approved'):
        conference = call.conference
        form = Form(name="{} CFP Form".format(conference.name))
        form.save()

        form.field_set.create(
            name='title',
            required=True,
            order=1,
        )

        form.field_set.create(
            name='abstract',
            required=True,
            widget=1,
            order=2,
        )

        if call.needs_audience:
            audience = form.field_set.create(
                name='audience',
                kind=3,
                required=True,
                order=5,
            )
            audience.option_set.create(value='Beginner')
            audience.option_set.create(value='Intermidiate')
            audience.option_set.create(value='Advancded')

        if conference.track_set.count():
            field = form.field_set.create(
                name='track',
                kind=3,
                required=True,
                order=4,
            )
            for track in conference.track_set.all():
                field.option_set.create(value=track.name)

        if conference.format_set.count():
            field = form.field_set.create(
                name='format',
                kind=3,
                required=True,
                order=3,
            )
            for fmt in conference.format_set.all():
                field.option_set.create(value=fmt.name)

        call.form = form
        call.save()

    Talk = apps.get_model("cfp", "Talk")
    Submission = apps.get_model("formbuilder", "Submission")

    for talk in Talk.objects.all():
        print(talk.title)
        sub = Submission(form=talk.call.form)
        sub.save()

        for field in talk.call.form.field_set.all():
            if field.name == 'title':
                sub.entry_set.create(
                    field=field,
                    value=talk.title,
                )

            if field.name == 'abstract':
                sub.entry_set.create(
                    field=field,
                    value=talk.abstract
                )

            if field.name == 'track':
                sub.entry_set.create(
                    field=field,
                    value=talk.track.name,
                )

            if field.name == 'audience':
                levels = dict([
                    (1, 'Beginner'),
                    (2, 'Intermidiate'),
                    (3, 'Advancded'),
                ])

                sub.entry_set.create(
                    field=field,
                    value=levels.get(talk.audience, 'Beginner'),
                )
            if field.name == 'format':
                sub.entry_set.create(
                    field=field,
                    value=talk.format.name,
                )

        talk.submission = sub
        talk.save()


@transaction.atomic
def delete_forms_and_submissions(apps, schema_editor):
    Talk = apps.get_model("cfp", "Talk")
    for talk in Talk.objects.filter(submission__isnull=False):
        talk.submission = None
        talk.save()

    Call = apps.get_model("cfp", "Call")
    for call in Call.objects.filter(form__isnull=False):
        call.form = None
        call.save()

    Submission = apps.get_model("formbuilder", "Submission")
    Form = apps.get_model("formbuilder", "Form")

    Submission.objects.all().delete()
    Form.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0025_auto_20150227_0848'),
    ]

    operations = [
        migrations.RunPython(create_forms_and_submissions,
                             delete_forms_and_submissions),
    ]
