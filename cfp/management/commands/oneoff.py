from django.core.management.base import BaseCommand
from django.db import transaction

from cfp.models import Call


class Command(BaseCommand):
    help = 'Migrate descriptions to Calls'

    def handle(self, *args, **options):
        for call in Call.objects.all():
            if len(call.description) > 0:
                continue
            if len(call.conference.description) == 0:
                continue

            call.description = call.conference.description
            call.conference.description = ""

            with transaction.atomic():
                call.save()
                call.conference.save()
                self.stdout.write("updated " + call.conference.name)
