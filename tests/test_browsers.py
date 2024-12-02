import os
import sys
import unittest
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from downedit.service.browsers import Browser

class TestBrowser(unittest.TestCase):

    @patch('random.choice')
    def test_chrome_version(self, mock_choice):
        mock_choice.return_value = '100.0.4896'
        browser = Browser(browser="chrome")
        version = browser.get_version()
        print(f"Chrome Version: {version}")
        self.assertEqual(version["major"], '100.0.4896')
        self.assertIn("webkit", version)
        self.assertEqual(version["webkit"], '537.36')

    @patch('random.choice')
    def test_firefox_version(self, mock_choice):
        mock_choice.return_value = '103.0'
        browser = Browser(browser="firefox")
        version = browser.get_version()
        print(f"Firefox Version: {version}")
        self.assertEqual(version["major"], '103.0')
        self.assertIn("minor", version)
        self.assertTrue(0 <= version["minor"] <= 2)

    @patch('random.choice')
    def test_edge_version(self, mock_choice):
        mock_choice.return_value = '100.0.1185'
        browser = Browser(browser="edge")
        version = browser.get_version()
        print(f"Edge Version: {version}")
        self.assertEqual(version["major"], '100.0.1185')
        self.assertIn("webkit", version)
        self.assertEqual(version["webkit"], '537.36')

    @patch('random.choice')
    def test_safari_version(self, mock_choice):
        mock_choice.return_value = '10'
        browser = Browser(browser="safari")
        version = browser.get_version()
        print(f"Safari Version: {version}")
        self.assertEqual(version["major"], '10')
        self.assertIn("webkit", version)
        self.assertEqual(version["webkit"], '602.4.8')

    def test_invalid_browser(self):
        browser = Browser(browser="invalid_browser")
        version = browser.get_version()
        print(f"Invalid Browser Version: {version}")
        self.assertIn("major", version)
        self.assertIn("webkit", version)

if __name__ == '__main__':
    unittest.main()