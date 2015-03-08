import random
import string
from datetime import datetime, timedelta

from django.utils import text
from django.utils import timezone
from django.contrib.auth.models import User

from cfp import models

WORDS = open("/usr/share/dict/words").read().splitlines()


def random_string(size):
    return ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for _ in range(size))


def get_paragraph():
    return ' '.join([get_sentence() for _ in range(4)])


def get_sentence():
    words = [random.choice(WORDS).lower() for _ in range(8)]
    words[0] = words[0].title()
    return ' '.join(words) + '.'


def get_name():
    return ' '.join([random.choice(WORDS).title() for _ in range(2)])


def make_user(username=None):
    username = username or random_string(25)
    return User.objects.create(username=username)


def make_call(conference=None, created=None, country='US',
              start=None, end=None, state='approved', description=None):
    created = created or timezone.now()
    conference = conference or make_conference()
    start = start or datetime.today() - timedelta(days=2)
    end = end or datetime.today() + timedelta(days=2)
    notify = end or datetime.today() + timedelta(days=9)
    description = description or get_paragraph()
    return models.Call.objects.create(
        conference=conference,
        created=created,
        start=start,
        end=end,
        notify=notify,
        description=description,
        state=state,
    )


def make_conference(country='US', start=None, slug=None, end=None, name=None,
                    twitter_handle='example', twitter_hashtag='example',
                    website_url='conf.example.com', city='Tahoe',
                    tagline=None, description=None):
    name = name or get_name() + ' Con'
    slug = slug or text.slugify(name)
    start = start or datetime.today()
    end = end or datetime.today()
    tagline = tagline or get_sentence()
    description = description or get_paragraph()
    return models.Conference.objects.create(
        name=name,
        start=start,
        end=end,
        city=city,
        country=country,
        slug=slug,
        tagline=tagline,
        description=description,
        website_url=website_url,
        twitter_handle=twitter_handle,
        twitter_hashtag=twitter_hashtag,
    )


def make_profile(owner=None, email_address=None, name=None):
    owner = owner or make_user()
    name = owner.first_name or name or random_string(10)
    email_address = email_address or owner.email or \
        "{}@example.com".format(random_string(5))
    return models.Profile.objects.create(
        owner=owner,
        email_address=email_address,
        name=name,
    )


def make_saved_search(created=None, owner=None, country='US'):
    created = created or timezone.now()
    owner = owner or make_user()
    return models.SavedSearch.objects.create(
        created=created,
        owner=owner,
        country=country,
    )


def make_user_mailing(created=None, owner=None, call=None):
    created = created or timezone.now()
    owner = owner or make_user()
    call = call or make_call()
    return models.UserMailing.objects.create(
        created=created,
        owner=owner,
        call=call,
    )
