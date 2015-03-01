import os
import subprocess as sh

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Import the production database locally'

    def handle(self, *args, **options):
        if not os.environ['ENVIRONMENT'] == 'DEVELOPMENT':
            raise ValueError('This command can only be run in development')

        try:
            sh.check_call(['dropdb', 'speakers'])
            sh.check_call(['createdb', 'speakers'])
            sh.check_call(['heroku', 'pgbackups:capture'])
            url = sh.check_output(['heroku', 'pgbackups:url'])
            sh.check_call(['curl', '-o', 'latest.dump', url])
            sh.call(['pg_restore', '--verbose', '--clean', '--no-acl',
                     '--no-owner', '-j', '2', '-h', 'localhost', '-d',
                     'speakers', 'latest.dump'])
        finally:
            if os.path.exists('latest.dump'):
                os.unlink('latest.dump')
