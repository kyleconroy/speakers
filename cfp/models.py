from datetime import datetime
import urllib.parse

from django.db import models
from django.core.urlresolvers import reverse

from django_countries.fields import CountryField
from django_fsm import FSMField, transition


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