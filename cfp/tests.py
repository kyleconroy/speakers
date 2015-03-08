from django.test import TestCase

from cfp import models, search


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


class SearchTest(TestCase):
    def test_single_quotes(self):
        self.assertEquals(['foo', 'foo bar', 'baz'],
                          search.tokenize_query("'foo' 'foo bar' baz"))

    def test_double_quotes(self):
        self.assertEquals(['foo bar', 'baz'],
                          search.tokenize_query('"foo bar" baz'))

    def test_whitespace(self):
        self.assertEquals(['hello'], search.tokenize_query("    hello "))

    def test_colons(self):
        self.assertEquals(['foo', 'location:us', 'topic:python'],
                          search.tokenize_query("foo location:us topic:python"))

    def test_filters(self):
        self.assertEquals([['location', 'us'], ['topic', 'python']],
                          search.filters("foo location:us topic:python"))
