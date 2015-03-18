import os

from django.core.management.base import BaseCommand, CommandError

from raven import Client


class SentryCommand(BaseCommand):
    def execute(self, *args, **options):
        try:
            return super(SentryCommand, self).execute(*args, **options)
        except Exception as e:
            if not isinstance(e, CommandError):
                if 'SENTRY_DSN' in os.environ:
                    dsn = os.environ['SENTRY_DSN']
                else:
                    raise
                sentry = Client(dsn)
                sentry.get_ident(sentry.captureException())
