import string
from datetime import datetime
import random
import urllib.parse

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django_countries.fields import CountryField
from django_fsm import FSMField, transition


def token(size):
    c = string.ascii_uppercase + string.digits
    return ''.join(random.SystemRandom().choice(c) for _ in range(size))


class Topic(models.Model):
    value = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name


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

    twitter_handle = models.CharField(max_length=20, blank=True)
    twitter_hashtag = models.CharField(max_length=20, blank=True)
    topics = models.ManyToManyField(Topic)

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
                                self.end.strftime("%d, %Y"))

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
    form = models.ForeignKey('formbuilder.Form', null=True)

    # If true, we'll show the form on the website. Otherwise
    # just post a link to the talk
    hosted = models.BooleanField(default=False)

    def __str__(self):
        return "{} CFP".format(self.conference)

    def get_absolute_url(self):
        return reverse('call_read',
                       args=[self.conference.slug, self.conference.start.year])

    def is_open(self):
        return self.days_left() >= 0

    def days_left(self):
        return (self.end - datetime.utcnow().date()).days

    def iframe_url(self):
        if 'docs.google.com' in self.application_url:
            return self.application_url + "?embedded=true"
        if 'typeform.com' in self.application_url:
            return self.application_url
        return None

    @transition(field=state, source='new', target='spam')
    def quarantine(self):
        pass

    @transition(field=state, source='new', target='approved')
    def approve(self):
        pass

    @transition(field=state, source='*', target='rejected')
    def reject(self):
        pass


class Talk(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    submission = models.ForeignKey('formbuilder.Submission', null=True)
    token = models.CharField(max_length=15, unique=True)
    title = models.CharField(max_length=300)
    call = models.ForeignKey('Call')
    profile = models.ForeignKey('Profile')
    state = FSMField(default='new', protected=True, db_index=True)

    def __str__(self):
        return self.title

    @transition(field=state, source='new', target='submitted')
    def submit(self):
        pass

    def get_absolute_url(self):
        return reverse('talk_read', args=[self.id])

    def get_admin_url(self):
        return reverse('submission_read', args=[self.id])


class Profile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=300)
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
        if not profile.name:
            profile.name = "{} {}".format(user.first_name, user.last_name)
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
            len(self.name) == 0))
