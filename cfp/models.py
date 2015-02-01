from django.db import models
from django_countries.fields import CountryField


class Conference(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(max_length=45, db_index=True)
    name = models.CharField(max_length=45)
    venue = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    country = CountryField()
    state = models.CharField(max_length=100)
    tagline = models.CharField(max_length=250)
    description = models.TextField()
    twitter_handle = models.CharField(max_length=15, blank=True)
    twitter_hashtag = models.CharField(max_length=20, blank=True)
    start = models.DateField(db_index=True)
    end = models.DateField(db_index=True)
    maps_url = models.URLField(max_length=300, blank=True)
    website_url = models.URLField()
    conduct_url = models.URLField(blank=True)
    call = models.ForeignKey('Call')


class Call(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    start = models.DateField()
    end = models.DateField()
    notify = models.DateField(blank=True)
    lanyrd_url = models.URLField(blank=True)
