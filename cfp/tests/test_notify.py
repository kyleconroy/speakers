from datetime import timedelta
import unittest

from django.test import TestCase
from django.utils import timezone

from cfp import search, fakedata
from cfp.management.commands import notify


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
