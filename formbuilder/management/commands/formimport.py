from django.core.management.base import BaseCommand

import requests

from formbuilder import importers


class Command(BaseCommand):
    help = 'Import a Google form'

    def handle(self, url, **kwargs):
        resp = requests.get(url)
        form = importers.parse_google_form(resp.content)
        self.stdout.write(form.name)
