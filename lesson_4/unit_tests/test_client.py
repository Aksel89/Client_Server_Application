import unittest

from lesson_4.client import create_presence, process_ans
from lesson_4.common.variables import TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, ENCODING

import os
import sys



class TestClient(unittest.TestCase):
    """
    Тесты клиента.
    """
    variables = {
        'good_request': '200 OK',
        'bad_request': '400 BAD REQUEST',
        'test_request': {
            ACTION: PRESENCE,
            TIME: 1645387814,
            USER: {
                ACCOUNT_NAME: 'test',
            },
            'encoding': ENCODING
        },
    }

    def test_create_presence(self):
        """
        Корректность запроса.
        :return:
        """
        test = create_presence()
        test[TIME] = 1645387814
        self.assertEqual(test, self.variables['test_request'])

    def test_200_ok(self):

        self.assertEqual(process_ans({RESPONSE: 200}), self.variables['good_request'])

    def test_400_bad(self):

        self.assertEqual(process_ans({RESPONSE: 400}), self.variables['bad_request'])

    def test_server_error(self):

        self.assertEqual(ValueError, process_ans, {ERROR: 'BAD REQUEST'})


if __name__ == '__main__':
    unittest.main()
