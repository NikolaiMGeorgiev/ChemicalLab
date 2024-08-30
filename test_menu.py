import unittest
from unittest import TestCase
from unittest.mock import patch
from io import StringIO
from menu import Menu
from database import DB

def save_to_file(content, filename):
    with open(f'tests/{filename}.txt', 'w') as f:
        f.write(content)

def read_from_file(filename):
    with open(f'tests/{filename}.txt', 'r') as f:
        content = f.read()
    return content

class TestMenu(TestCase):
    def setUp(self):
        self.db = DB()
        self.user = {"id": -1, "name": "Test", "type": "user"}
        self.menu = Menu(self.db, self.user)

    def test_get_valid_number_out_of_bounds(self):
        with patch('builtins.input', side_effect=["10", "-1", "abcd", "", "   ", "\n", "1"]), patch('sys.stdout', new=StringIO()) as mock_stdout:    
            self.menu.get_valid_number(4, "")
            self.assertEqual(mock_stdout.getvalue().strip(), "Invalid option! Try again.\n" * 5 + "Invalid option! Try again.")

    def test_check_for_exit_command_exit(self):
        with patch('builtins.exit') as mock_exit:
            self.menu.check_for_exit_command("/exit")
            mock_exit.assert_called_once()

    @patch.object(Menu, 'clear')
    @patch.object(Menu, 'init_menu')
    def test_check_for_exit_command_menu(self, mock_init_menu, mock_clear):
        self.menu.check_for_exit_command("/menu")
        mock_clear.assert_called_once()
        mock_init_menu.assert_called_once()

    def diary_page_command(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout, patch('builtins.input', side_effect = ['1', '/p']):
            menu = Menu()
            menu.init_menu()
            mockup_data = read_from_file('test_diary_page_command')
            self.assertEqual(mock_stdout.getvalue().strip(), f'{self.munu_string}{mockup_data}')
    
if __name__ == "__main__":
    unittest.main()
