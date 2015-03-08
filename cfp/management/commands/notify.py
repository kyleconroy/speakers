from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.template import Context

import requests

from cfp.models import UserMailing, Profile
from cfp import search


class Command(BaseCommand):
    help = 'Send notification emails to users'

    def send_notification(self, user, profile, call, saved_search):
        subject = "The {} call for speakers is open".format(
            call.conference.name)

        text = get_template('cfp/email/open_call.txt').render(
            Context({
                'call': call,
                'conf': call.conference,
                'saved_search': saved_search,
            })
        )

        resp = requests.post(
            "https://api.mailgun.net/v2/calltospeakers.com/messages",
            auth=("api", settings.MAILGUN_KEY),
            data={
                "from": "Call to Speakers <robot@calltospeakers.com>",
                "to": [profile.email_address],
                "subject": subject,
                "text": text,
                "h:Reply-To": "contact@calltospeakers.com",
            })
        resp.raise_for_status()

        return UserMailing.objects.create(
            owner=user,
            call=call,
            email=profile.email_address,
            subject=subject,
            text='FOO'
        )

    def handle(self, *args, **options):
        for user in User.objects.all():
            profile = Profile.objects.filter(owner=user).first()
            for saved_search, call in search.find_new_calls(user):
                self.send_notification(user, profile, call, saved_search)
                continue
