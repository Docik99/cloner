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
