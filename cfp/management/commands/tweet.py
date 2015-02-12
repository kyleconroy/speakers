from datetime import datetime, timedelta
import os

from django.core.management.base import BaseCommand

import tweepy

from cfp.models import Call


class Command(BaseCommand):
    help = 'Tweet out CFPs'

    def messages(self, call):
        n = call.conference.name
        a = call.conference.twitter_handle
        h = call.conference.twitter_hashtag
        l = "https://calltospeakers.com" + call.get_absolute_url()

        if h and a:
            yield "{} call for speakers is now open {} @{} #{}".format(n, l, a, h)

        if a:
            yield "{} call for speakers is now open {} @{}".format(n, l, a)

        yield "{} call for speakers is now open {}".format(n, l)
        yield "{} call for speakers is now open {}".format(n[:85], l)

    def handle(self, *args, **options):
        consumer_key = os.environ['TWITTER_CONSUMER_KEY']
        consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
        access_token = os.environ['TWITTER_ACCESS_TOKEN']
        access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.secure = True
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth, api_root='/1.1')

        last_tweet = api.user_timeline()[0]

        if (datetime.utcnow() - last_tweet.created_at) < timedelta(hours=3):
            self.stdout.write("skipping last tweet was less than 3 hours ago")
            return

        call = Call.objects.filter(tweet_id=0, state='approved',
                                   start__lte=datetime.utcnow(),
                                   end__gte=datetime.utcnow()).\
            order_by('-created')[0]

        for message in self.messages(call):
            try:
                tweet = api.update_status(None, status=message)
            except tweepy.error.TweepError:
                self.stdout.write("errored tweet={}".format(message))
                continue

            call.tweet_id = tweet.id
            call.save()
            self.stdout.write("tweeted tweet={}".format(tweet.id))
            return
