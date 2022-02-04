import os
import sys
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from common.utils import get_message, send_message
from client import create_presence, process_ans

class TestClass(unittest.TestCase):
    """
    Класс с тестами
    """

    def test_def_presence(self):
        """Тест корректного запроса"""
        test = create_presence()
        test[TIME] = 1.1
        self.assertEqual(test, {ACTION: PRESENCE, TIME:1.1, USER:{ACCOUNT_NAME: 'Guest'}})

    def test_200_ans(self):
        """Тест корректного разбора ответа 200"""
        self.assertEqual(process_ans({RESPONSE: 200}), '200 : OK')

    def test_400_ans(self):
        """Тест коректного разбора ответа 400"""
        self.assertEqual(process_ans({RESPONSE:400, ERROR: 'Bad Request'}), '400 : Bad Request')

    def test_no_response(self):
        """Тест исключения без поля RESPONSE"""
        self.assertRaises(ValueError, process_ans, {ERROR: 'Bad Request'})

    def test_time_mark_in(self):
        """Проверка наличия метки времени"""
        self.assertIn(TIME, create_presence())

    def test_time_mark_not_in(self):
        """Проверка наличия отсутстсвия =) метки времени"""
        test = create_presence()
        del test[TIME]
        self.assertNotIn(TIME, test)

    def test_presence_is_dict(self):
        """Проерка, является ли presence словарем"""
        self.assertIsInstance(create_presence(), dict)

    def test_time_is_float(self):
        """Проверка, является ли тип TIME float"""
        self.assertIsInstance(create_presence()[TIME], float)

    def test_time_is_not_string(self):
        """Проверкв, не является ли TIME строкой"""
        self.assertNotIsInstance(create_presence()[TIME], str)


if __name__ == '__main__':
    unittest.main()