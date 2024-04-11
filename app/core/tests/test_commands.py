from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError
from django.test import SimpleTestCase
from unittest.mock import patch
from django.core.management import call_command

from time import sleep

@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):

    
    def test_wait_for_db_ready(self, patched_check):
        "A test case for ready database"
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(database=['default'])

    
    @patch('time.sleep')
    def test_wait_for_db(self,patched_sleep, patched_check):
        "A test case for a starting database"
        patched_check.side_effect = [Psycopg2OpError]*2 + [OperationalError]*3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(database=['default'])