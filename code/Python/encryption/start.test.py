import unittest
from unittest.mock import patch
import sys
import io
from colorama import Fore, Style, init
from start import clear_terminal, banner, help_menu, main

# Initialize colorama
init(autoreset=True)

class TestStart(unittest.TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_banner(self, mock_stdout):
        """Test that the banner function prints the expected output."""
        banner()
        output = mock_stdout.getvalue()
        self.assertIn("______", output)  # Check if the banner contains the word "______"

    @patch('os.system')
    def test_clear_terminal_windows(self, mock_system):
        """Test that clear_terminal calls 'cls' on Windows."""
        with patch('os.name', 'nt'):
            clear_terminal()
            mock_system.assert_called_with('cls')

    @patch('os.system')
    def test_clear_terminal_unix(self, mock_system):
        """Test that clear_terminal calls 'clear' on Unix-based systems."""
        with patch('os.name', 'posix'):
            clear_terminal()
            mock_system.assert_called_with('clear')

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_help_menu(self, mock_stdout):
        """Test that help_menu prints the expected help information."""
        help_menu()
        output = mock_stdout.getvalue()
        self.assertIn("Usage: python start.py", output)  # Check if the help contains "Usage"

    @patch('sys.argv', ['start.py', 'encrypt', 'fernet', 'message', 'Hello', 'output.txt'])
    def test_arg_passed(self):
        """Test that a command-line argument is passed and correctly processed."""
        with self.assertRaises(SystemExit):  # Expecting the script to terminate after argument processing
            main()  # This will run the main function which processes command-line arguments

    @patch('sys.argv', ['start.py'])
    def test_no_arg_passed(self):
        """Test that the script correctly handles no command-line argument."""
        with self.assertRaises(SystemExit):  # Expecting the script to exit due to missing arguments
            main()  # This will run the main function which processes command-line arguments


# Custom test runner to display results in color
class ColorTestRunner(unittest.TextTestRunner):
    def getDescription(self, test):
        return str(test)

    def run(self, test):
        result = super().run(test)
        self.display_test_results(result)
        return result

    def display_test_results(self, result):
        for test, was_success in result.testsRun:
            if was_success:
                print(Fore.GREEN + f"{test} PASSED")
            else:
                print(Fore.RED + f"{test} FAILED")

if __name__ == '__main__':
    # Set verbosity to 2 to ensure all test output is printed and use custom color output
    unittest.main(verbosity=2, testRunner=ColorTestRunner())
