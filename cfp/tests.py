from django.test import TestCase

from cfp import models

class TokenTestCase(TestCase):
    def test_token_len(self):
        self.assertEquals(10, len(models.token(10)))

    def test_token_not_same(self):
        self.assertNotEquals(models.token(10), models.token(10))
