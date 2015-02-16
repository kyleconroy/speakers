import string
from datetime import datetime
import random
import urllib.parse

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django_countries.fields import CountryField
from django_fsm import FSMField, transition

from cfp import constants


def token(size):
    c = string.ascii_uppercase + string.digits
    return ''.join(random.SystemRandom().choice(c) for _ in range(size))


class Conference(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    slug = models.CharField(max_length=100, db_index=True)
    legacy_slug = models.CharField(max_length=100, db_index=True, blank=True)
    name = models.CharField(max_length=200)

    venue_name = models.CharField(max_length=100, blank=True)
    venue_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    country = CountryField(default='US')
    state = models.CharField(max_length=100, blank=True)

    tagline = models.CharField(max_length=255)
    description = models.TextField()
    programming_language = models.CharField(max_length=30, db_index=True,
        choices=constants.PROGRAMMING_LANGUAGES, default='', blank=True)

    twitter_handle = models.CharField(max_length=20, blank=True)
    twitter_hashtag = models.CharField(max_length=20, blank=True)

    start = models.DateField(db_index=True)
    end = models.DateField(db_index=True)

    maps_url = models.URLField(max_length=1000, blank=True)
    website_url = models.URLField(max_length=500)
    conduct_url = models.URLField(max_length=500, blank=True)
    lanyrd_url = models.URLField(max_length=500, blank=True)

    def website_domain(self):
        return urllib.parse.urlparse(self.website_url).netloc

    def __str__(self):
        return "{} {}".format(self.name, self.start.year)

    def date_range(self):
        if (self.end - self.start).days == 0:
            return self.start.strftime("%b %d, %Y")
        return "{} - {}".format(self.start.strftime("%b %d"),
                                self.start.strftime("%d, %Y"))

    def get_absolute_url(self):
        return reverse('call_read', args=[self.slug, self.start.year])

    class Meta:
        unique_together = ('slug', 'start')
        ordering = ['slug', 'start']


class Call(models.Model):
    conference = models.ForeignKey('Conference')
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    start = models.DateField(db_index=True)
    end = models.DateField(db_index=True)
    notify = models.DateField(blank=True)
    lanyrd_url = models.URLField(max_length=500, blank=True)
    application_url = models.URLField(max_length=1000, blank=True)
    tweet_id = models.BigIntegerField(db_index=True, default=0)
    state = FSMField(default='new', protected=True, db_index=True)

    # These fields are used for the submission form,
    # probably want to do something better here in the future
    needs_audience = models.BooleanField(default=False)

    def __str__(self):
        return "{} CFP".format(self.conference)


    def get_absolute_url(self):
        return reverse('call_read',
                       args=[self.conference.slug, self.conference.start.year])

    def is_open(self):
        return self.days_left() >= 0

    def days_left(self):
        return (self.end - datetime.utcnow().date()).days

    @transition(field=state, source='new', target='spam')
    def quarantine(self):
        pass

    @transition(field=state, source='new', target='approved')
    def approve(self):
        pass

    @transition(field=state, source='*', target='rejected')
    def reject(self):
        pass


class Track(models.Model):
    conference = models.ForeignKey('Conference')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

LEVELS = ((1, 'Beginner'), (2, 'Intermidiate'), (3, 'Advancded'))


class Talk(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=15, unique=True)
    title = models.CharField(max_length=300)
    track = models.ForeignKey('Track', null=True, blank=True)
    call = models.ForeignKey('Call')
    profile = models.ForeignKey('Profile')
    abstract = models.TextField()
    audience = models.IntegerField(choices=LEVELS, default=1, blank=True)
    state = FSMField(default='new', protected=True, db_index=True)

    def __str__(self):
        return self.title

    @transition(field=state, source='new', target='submitted')
    def submit(self):
        pass

    def get_absolute_url(self):
        return reverse('talk_read', args=[self.id])


class Profile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, null=True)
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    email_address = models.EmailField(max_length=254)

    bio = models.TextField(blank=True)
    personal_website = models.URLField(max_length=500, blank=True)
    twitter_handle = models.CharField(max_length=20, blank=True)
    github_handle = models.CharField(max_length=20, blank=True)
    organization = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=60, blank=True)
    country = CountryField(default='US')

    @classmethod
    def generate(cls, user):
        try:
            profile = cls.objects.get(owner=user)
        except cls.DoesNotExist:
            profile = cls(owner=user)
        if not profile.first_name:
            profile.first_name = user.first_name
        if not profile.last_name:
            profile.last_name = user.last_name
        if not profile.email_address:
            profile.email_address = user.email
        return profile

    def __str__(self):
        return self.email_address

    def is_empty(self):
        return any((
            len(self.bio) == 0,
            len(self.personal_website) == 0,
            len(self.twitter_handle) == 0,
            len(self.github_handle) == 0,
            len(self.organization) == 0,
            len(self.job_title) == 0,
            len(self.first_name) == 0,
            len(self.last_name) == 0))
