from datetime import timedelta
import unittest

from django.test import TestCase, SimpleTestCase
from django.utils import timezone

from cfp import models, search, fakedata
from cfp.management.commands import notify


class CFPTest(SimpleTestCase):
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


class NotifyTest(TestCase):

    def setUp(self):
        self.user = fakedata.make_user()
        self.profile = fakedata.make_profile(owner=self.user)

    def test_found_us_new(self):
        now = timezone.now()
        conf = fakedata.make_conference()
        call = fakedata.make_call(conference=conf, created=now)
        ss = fakedata.make_saved_search(owner=self.user,
                                        created=now - timedelta(days=1))

        results = search.find_new_calls(self.user)
        found_ss, found_call = next(results)

        self.assertIsNone(next(results, None))
        self.assertEquals(ss.pk, found_ss.pk)
        self.assertEquals(call.pk, found_call.pk)

    def test_found_zero_due_to_existing(self):
        now = timezone.now()
        conf = fakedata.make_conference()
        call = fakedata.make_call(conference=conf, created=now)
        fakedata.make_user_mailing(call=call, owner=self.user)
        fakedata.make_saved_search(owner=self.user,
                                   created=now - timedelta(days=1))
        self.assertIsNone(next(search.find_new_calls(self.user), None))

    def test_found_zero_due_to_created(self):
        now = timezone.now()
        conf = fakedata.make_conference()
        fakedata.make_call(conference=conf, created=now)
        fakedata.make_saved_search(owner=self.user,
                                   created=now + timedelta(days=1))
        self.assertIsNone(next(search.find_new_calls(self.user), None))

    @unittest.skip("Don't send email every test run")
    def test_send_email(self):
        user = fakedata.make_user()
        profile = fakedata.make_profile(owner=user,
                                        email_address="kyle@kyleconroy.com")
        ss = fakedata.make_saved_search(owner=self.user)
        call = fakedata.make_call()

        cmd = notify.Command()
        cmd.send_notification(user, profile, call, ss)
