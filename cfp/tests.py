from django.test import TestCase

from cfp import models


class CFPTest(TestCase):
    def test_token_len(self):
        self.assertEquals(10, len(models.token(10)))

    def test_token_not_same(self):
        self.assertNotEquals(models.token(10), models.token(10))

    def test_submit(self):
        talk = models.Talk()
        self.assertEquals('new', talk.state)
        talk.submit()
        self.assertEquals('submitted', talk.state)

    def test_google_docs_iframe_url(self):
        call = models.Call()
        call.application_url = ("https://docs.google.com/forms/d/10VztOmnh5Kx"
                                "zWnV4OFU2_6uicIDuh5XB-9WUJYqLjCw/viewform")
        iframe_url = ("https://docs.google.com/forms/d/10VztOmnh5KxzWnV"
                      "4OFU2_6uicIDuh5XB-9WUJYqLjCw/viewform?embedded=true")
        self.assertEquals(iframe_url, call.iframe_url())
