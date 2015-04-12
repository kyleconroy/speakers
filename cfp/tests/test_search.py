from django.test import SimpleTestCase

from cfp import search


class SearchTest(SimpleTestCase):
    def test_single_quotes(self):
        self.assertEquals(['foo', 'foo bar', 'baz'],
                          search.tokenize_query("'foo' 'foo bar' baz"))

    def test_double_quotes(self):
        self.assertEquals(['foo bar', 'baz'],
                          search.tokenize_query('"foo bar" baz'))

    def test_whitespace(self):
        self.assertEquals(['hello'], search.tokenize_query("    hello "))

    def test_colons(self):
        self.assertEquals(['foo', 'loc:us', 'topic:python'],
                          search.tokenize_query("foo loc:us topic:python"))

    def test_filters(self):
        self.assertEquals([['location', 'us'], ['topic', 'python']],
                          search.filters("foo location:us topic:python"))
