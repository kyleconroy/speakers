import os

from django.test import SimpleTestCase

from formbuilder import importers


class GoogleFormTest(SimpleTestCase):

    def test_parse_form(self):
        p = os.path.join(os.path.dirname(__file__), 'fixtures/jsconfbp.html')
        form = importers.parse_google_form(open(p))
        self.assertEquals(form, 'foo')
