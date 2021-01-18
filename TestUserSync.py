"""
tests for gitlab_user_sync
"""
import unittest
from unittest.mock import patch
import gitlab_user_sync

class ParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = gitlab_user_sync.create_args()

    def test_something(self):
        flag_list = ['--get', '-g', '--token', '-t']
        for i in range(4):
            parsed = self.parser.parse_args([flag_list[i], 'TestArg'])
            if i < 2:
                self.assertEqual(parsed.get, 'TestArg')
            else:
                self.assertEqual(parsed.token, 'TestArg')
