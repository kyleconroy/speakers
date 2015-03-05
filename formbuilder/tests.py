import os

from django.test import TestCase

from formbuilder import importers


class GoogleFormTest(TestCase):

    def load_fixture(self, f):
        return open(os.path.join(os.path.dirname(__file__), 'fixtures', f))

    def test_jsconfpb_form(self):
        form = importers.parse_google_form(self.load_fixture('jsconfbp.html'))
        self.assertNotEquals(0, len(form.field_set.all()))

    def test_puppetny_form(self):
        form = importers.parse_google_form(self.load_fixture('puppetny.html'))
        self.assertEquals(10, len(form.field_set.all()))
