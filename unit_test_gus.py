"""
tests for gitlab_user_sync

тестирование части НЕ взаимодействующей с сервером
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
            args = self.parser.parse_args([flag_list[i], 'TestArg' + str(i)])
            if i < 2:
                self.assertEqual(args.get, 'TestArg' + str(i))
            else:
                self.assertEqual(args.token, 'TestArg' + str(i))


class PasswordTest(unittest.TestCase):
    """Класс тестов для функции создания пароля"""

    def correct_pass(self):
        """Проверка генерации пароля заданной длины"""
        pas = gitlab_user_sync.generate_pass(5)
        self.assertEqual(5, len(pas))

    def negative_pass(self):
        self.assertRaises(Exception, gitlab_user_sync.generate_pass(-5))

    def str_pass(self):
        self.assertRaises(Exception, gitlab_user_sync.generate_pass("stroka"))


if __name__ == '__main__':
    unittest.main()
