import datetime

from django.db import transaction
from django.core.management.base import BaseCommand

from django_countries import countries
from bs4 import BeautifulSoup
import html2text
import requests

from cfp.models import Call, Conference


def normalize_handle(handle):
    for s in ["http://", "https://", "www.twitter.com/", "twitter.com/", "@"]:
        handle = handle.replace(s, "")
    return handle.strip()


def normalize_hashtag(hashtag):
    return hashtag.replace("#", "").strip()


class Command(BaseCommand):
    help = 'Import CFPs from Lanyrd'

    def lanyrd_calls(self):
        for i in range(1, 100):
            url = "http://lanyrd.com/calls/?page={}".format(i)
            self.stdout.write("fetching {}".format(url))
            resp = requests.get(url)
            if not resp.ok:
                return
            soup = BeautifulSoup(resp.content)
            for a in soup.select('ol.call-list li.call-list-open p strong a'):
                yield a['href']

    def parse_conference(self, url, lookup):
        self.stdout.write("fetching {}".format(url))

        resp = requests.get(url)
        if not resp.ok:
            self.stdout.write("errored {}".format(url))
            return None

        soup = BeautifulSoup(resp.content)
        conf = Conference()
        conf.lanyrd_url = url
        conf.slug = url.split("/")[-2]

        match = soup.select("div.primary h1.summary")
        if match:
            conf.name = match[0].text.strip()

        match = soup.select("div.primary h2.tagline")
        if match:
            conf.tagline = match[0].text.strip()[:255]

        match = soup.select("a.website")
        if match:
            conf.website_url = match[0]["href"].lower()

        match = soup.select("a.twitter")
        if match:
            conf.twitter_handle = normalize_handle(match[0]["href"])

        match = soup.select("a.twitter-search")
        if match:
            conf.twitter_hashtag = normalize_hashtag(match[0].text)

        match = soup.select("#event-description p")
        if match:
            conf.description = match[0].text.strip()

        match = soup.select("a.sub-place")
        if match:
            conf.city = match[0].text.strip()

        match = soup.select("span.place-context a")
        if not match:
            match = soup.select("p.prominent-place a")
        if match:
            if match[0].text in ["England", "Wales"]:
                conf.country = 'UK'
            else:
                conf.country = lookup.get(match[0].text, 'US')

        match = soup.select("#venues h3")
        if match:
            conf.venue_name = match[0].text.strip()

        match = soup.select("#venues a.map-icon")
        if match:
            icon = match[0]
            addr = icon.parent.previous_sibling.previous_sibling
            conf.maps_url = icon["href"]
            conf.venue_address = addr.text.strip()[:255]

        def parse_date(day):
            day = day.replace("Sept.", "Sep.")
            try:
                return datetime.datetime.strptime(day, "%b. %d, %Y").date()
            except ValueError:
                return datetime.datetime.strptime(day, "%B %d, %Y").date()

        abbr_start = soup.select("abbr.dtstart")
        abbr_end = soup.select("abbr.dtend")

        if abbr_start and abbr_end:
            conf.start = parse_date(abbr_start[0]["title"])
            conf.end = parse_date(abbr_end[0]["title"])
        elif abbr_start:
            conf.start = parse_date(abbr_start[0]["title"])
            conf.end = parse_date(abbr_start[0]["title"])

        return conf

    def parse_call(self, url):
        self.stdout.write("fetching {}".format(url))

        resp = requests.get(url)
        if not resp.ok:
            self.stdout.write("errored {}".format(url))
            return None

        call = Call()
        call.lanyrd_url = url

        soup = BeautifulSoup(resp.content)

        match = soup.select("div.description")
        if match:
            call.description = html2text.html2text(str(match[0]))

        match = soup.select("div.primary > p a")
        if match:
            call.application_url = match[0]["href"]

        def parse_date(day):
            if day.lower() == "today":
                return datetime.date.today()

            sfxs = ["1st", "2nd", "3rd", "4th", "5th", "6th",
                    "7th", "8th", "9th", "0th", "1th", "2th", "3th"]

            for sfx in sfxs:
                day = day.replace(sfx, sfx[:1])

            return datetime.datetime.strptime(day, "%d %B %Y").date()

        for feature in soup.select("li.number-feature.num-title"):
            kind = feature.find('span').text.lower().strip()
            day = feature.find('strong').text.strip()

            if "open" in kind:
                call.start = parse_date(day)
            elif "close" in kind:
                call.end = parse_date(day)
            elif "notification" in kind:
                call.notify = parse_date(day)

        if call.start is None:
            call.start = datetime.date.today()

        if call.notify is None:
            call.notify = call.end + datetime.timedelta(days=7)

        return call

    def handle(self, *args, **options):
        urls = Conference.objects.values_list('lanyrd_url', flat=True)
        seen = set(urls.all())

        country_lookup = {v: k for k, v in dict(countries).items()}

        for url in self.lanyrd_calls():
            conference_url, _ = url.split('calls/q')

            if conference_url in seen:
                self.stdout.write("skipping {}".format(url))
                continue

            seen.add(conference_url)

            conf = self.parse_conference(conference_url, country_lookup)
            if conf is None:
                self.stdout.write("errored {}".format(conference_url))
                continue

            try:
                e = Conference.objects.get(slug=conf.slug, start=conf.start)
                e.lanyrd_url = conf.lanyrd_url
                e.save()
                self.stdout.write("updated {}".format(conference_url))
                continue
            except Conference.DoesNotExist:
                pass

            call = self.parse_call(url)
            if call is None:
                self.stdout.write("error parsing call {}".format(url))
                continue

            with transaction.atomic():
                conf.save()
                call.conference = conf
                call.save()
