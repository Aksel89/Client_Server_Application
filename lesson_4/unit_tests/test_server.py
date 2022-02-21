import unittest


from lesson_4.server import process_client_message
from lesson_4.common.variables import TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, ENCODING


class TestServer(unittest.TestCase):
    """
    Тесты функций сервера.
    """

    variables_dict = {
        'bad_response': {
            RESPONSE: 400,
            ERROR: 'BAD RESPONSE',
        },
        'good_response': {RESPONSE: 200},
        'correct_message': {
            ACTION: PRESENCE,
            TIME: 1645387814,
            USER: {ACCOUNT_NAME: 'test'},
            'encoding': ENCODING,
        },
        'error_action_message': {
            TIME: 1645387814,
            USER: {ACCOUNT_NAME: 'test'},
            'encoding': ENCODING,
        },
        'incorrect_action_message': {
            ACTION: 'any action',
            TIME: 1645387814,
            USER: {ACCOUNT_NAME: 'test'},
            'encoding': ENCODING,
        },
        'message_time_error': {
            ACTION: PRESENCE,
            USER: {ACCOUNT_NAME: 'test'},
            'encoding': ENCODING,
        },
        'incorrect_message_time': {
            ACTION: PRESENCE,
            TIME: 'wrong time',
            USER: {ACCOUNT_NAME: 'test'},
            'encoding': ENCODING,
        },
        'message_user_error': {
            ACTION: PRESENCE,
            TIME: 1645387814,
            USER: {True: 'Unregistered user'},
            'encoding': ENCODING,
        },
        'unregistered_user_message': {
            ACTION: PRESENCE,
            TIME: 1645387814,
            USER: {ACCOUNT_NAME: 'Unregistered user'},
            'encoding': ENCODING,
        },
    }

    def test_correct_message(self):

        self.assertEqual(process_client_message(self.variables_dict['correct_message']), self.variables_dict['bad_response'])

    def test_error_action_message(self):

        self.assertEqual(process_client_message(self.variables_dict['error_action_message']), self.variables_dict['bad_response'])

    def test_incorrect_action_message(self):

        self.assertEqual(process_client_message(
            self.variables_dict['incorrect_action_message']), self.variables_dict['bad_response'])

    def test_message_time_error(self):

        self.assertEqual(process_client_message(self.variables_dict['message_time_error']), self.variables_dict['bad_response'])

    def test_incorrect_message_time(self):

        self.assertEqual(process_client_message(
            self.variables_dict['incorrect_message_time']), self.variables_dict['bad_response'])

    def test_message_user_error(self):

        self.assertEqual(process_client_message(self.variables_dict['message_user_error']), self.variables_dict['bad_response'])

    def test_unregistered_user_message(self):

        self.assertEqual(process_client_message(
            self.variables_dict['unregistered_user_message']), self.variables_dict['bad_response'])


if __name__ == '__main__':
    unittest.main()
