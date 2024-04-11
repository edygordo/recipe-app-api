from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as psycopg2OpError
from django.db.utils import OperationalError


class Command(BaseCommand):
    "Django command for wait db"

    def handle(self, *args, **options):
        """ Entrypoint for command """
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (psycopg2OpError, OperationalError): # noqa
                self.stdout.write("Database unavailable,waiting for 1 second...") # noqa

        self.stdout.write(self.style.SUCCESS('Database available'))
