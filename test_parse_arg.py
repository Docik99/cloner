"""
tests for gitlab_user_sync
"""
import unittest
import gitlab_user_sync


class ParserTest(unittest.TestCase):
    """Класс тестов для работы с parser"""
    def setUp(self):
        self.parser = gitlab_user_sync.create_args()


    def test_arg(self):
        """Проверка корректности чтения аргументов"""
        flag_list = ['--get', '-g', '--token', '-t']
        for i in range(4):
            args = self.parser.parse_args([flag_list[i], 'TestArg'])
            if i < 2:
                self.assertEqual(args.get, 'TestArg')
            else:
                self.assertEqual(args.token, 'TestArg')

class UserTest(unittest.TestCase):
    def setUP(self):
        self.parser = gitlab_user_sync.create_args()


    def test_users(self):

        args = self.parser.parse_args(['--token', 'TestArg2'])
        self.response = gitlab_user_sync.get_user(args)
        self.response = open("user_data.json", 'r')
        self.assertEqual(6, self.response.other_web_url)
