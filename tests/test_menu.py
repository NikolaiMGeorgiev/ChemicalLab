import re
import sys
import unittest
from unittest import TestCase
from unittest.mock import patch, call, Mock
from io import StringIO
from menu import init_menu

def save_to_file(content, filename):
    with open(f'tests/{filename}.txt', 'w') as f:
        f.write(content)

def read_from_file(filename):
    with open(f'tests/{filename}.txt', 'r') as f:
        content = f.read()
    return content

class TestMenu(TestCase):
    # @patch('builtins.input', side_effect=['5', 'exit'])
    # @patch('os.system')
    # def test_invalid_input_exit(self, mock_os_system, mock_input):
    #     with patch('sys.stdout', new=StringIO()) as fake_out:
    #         init_menu()
    #         self.assertEqual(fake_out.getvalue().strip(), 'Invalid command')
    #         mock_os_system.assert_called_with('cls' if os.name == 'nt' else 'clear')

    # @patch('builtins.input', side_effect=['1', 'command1', 'exit'])
    # @patch('os.system')
    # def test_valid_input_command_exit(self, mock_os_system, mock_input):
    #     with patch('sys.stdout', new=StringIO()) as fake_out:
    #         init_menu()
    #         self.assertEqual(fake_out.getvalue().strip(), '1. Diary logs\n2.Lab\n3.Distributors\n4.User info\nSelect page by index:')
    #         mock_os_system.assert_called_with('cls' if os.name == 'nt' else 'clear')

    # @patch('builtins.input', side_effect=['10'])  # Mocking input function to return '10'
    # @patch('builtins.input', side_effect=['10'])
    # @patch('sys.stdout', new_callable=StringIO)
    # @patch('builtins.input', create=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.munu_string = '1. Diary logs\n2.Lab\n3.Distributors\n4.User info\nSelect page by index:\n'
    
    def tearDown(self):
        # Clean up your test environment here.
        # This could involve deleting test data, disconnecting from the database, etc.
        sys.exit()

    def test_page_out_of_bounds(self, input_value):
        with patch('sys.stdout', new=StringIO()) as mock_stdout, patch('builtins.input', return_value=input_value):
            init_menu()
            self.assertEqual(mock_stdout.getvalue().strip(), f'{self.munu_string}Invalid command')

    def test_diary_page_command(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout, patch('builtins.input', side_effect = ['1', '/p']):
            init_menu()
            mockup_data = read_from_file('test_diary_page_command')
            self.assertEqual(mock_stdout.getvalue().strip(), f'{self.munu_string}{mockup_data}')

def test_page_out_of_bounds():
    tester.test_page_out_of_bounds('10')
    tester.test_page_out_of_bounds('-1')
    tester.test_page_out_of_bounds('abcd')
    tester.test_page_out_of_bounds('')
    tester.test_page_out_of_bounds('   ')
    tester.test_page_out_of_bounds('\n')
    
tester = TestMenu()
test_page_out_of_bounds()
tester.test_diary_page_command()
