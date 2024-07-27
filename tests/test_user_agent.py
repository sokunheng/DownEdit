import unittest
from unittest.mock import MagicMock

from downedit.service.browsers import Browser, Chrome, Edge, Firefox, Safari
from downedit.service.platforms import Platform
from downedit.service.user_agents import UserAgent, version

class TestUserAgent(unittest.TestCase):

    def test_version_with_minor(self):
        self.assertEqual(version({'major': 10, 'minor': 5}), '10.5')

    def test_version_without_minor(self):
        self.assertEqual(version({'major': 10}, strip_zero=True), '10')

    def test_version_strip_zero(self):
        self.assertEqual(version({'major': 10, 'minor': 0}, strip_zero=True), '10')

    def test_user_agent_generation_windows_chrome(self):
        self._test_user_agent_generation("desktop", "windows", "chrome", 
                                        "Mozilla/5.0", "Windows NT", "AppleWebKit", "Chrome", "Safari")

    def test_user_agent_generation_android_chrome(self):
        self._test_user_agent_generation("mobile", "android", "chrome",
                                        "Mozilla/5.0", "Linux; Android", "AppleWebKit", "Chrome", "Mobile Safari")

    def test_user_agent_generation_macos_safari(self):
        self._test_user_agent_generation("desktop", "macos", "safari",
                                        "Mozilla/5.0", "Macintosh; Intel Mac OS X 10", "AppleWebKit", "Version", "Safari")

    def _test_user_agent_generation(self, platform_type, device_type, browser_type, *expected_substrings):
        # Mock the Browser and Platform classes
        mock_browser = MagicMock(spec=Browser)
        mock_platform = MagicMock(spec=Platform)

        # Set up return values for mocked methods based on platform and browser
        mock_platform.get_version.return_value = self._get_mock_platform_version(platform_type, device_type)
        mock_browser.get_version.return_value = self._get_mock_browser_version(browser_type)
        mock_browser.get_user_agents.return_value = self._get_mock_user_agents(browser_type)

        # Create a UserAgent instance with mocked dependencies
        user_agent = UserAgent(platform_type=platform_type, device_type=device_type, browser_type=browser_type)
        user_agent.browser = mock_browser
        user_agent.platform = mock_platform

        # Generate the user agent string
        generated_ua = user_agent.generate()

        # Assertions
        for substring in expected_substrings:
            self.assertIn(substring, generated_ua)

    def _get_mock_platform_version(self, platform_type, device_type):
        if platform_type == "desktop":
            if device_type == "windows":
                return {'major': '10', 'minor': '0'}
            elif device_type == "macos":
                return {'major': '10', 'minor': '15', 'build_number': '21F79'}
            elif device_type == "linux":
                return {'major': '5', 'minor': '19'}
        elif platform_type == "mobile":
            if device_type == "android":
                return {'major': '11', 'minor': '0', 'platform_model': 'SM-G991B', 'build_number': 'RP1A.200720.012'} 
            elif device_type == "ios":
                return {'major': '15', 'minor': '4'}
        return {}

    def _get_mock_browser_version(self, browser_type):
        if browser_type == "chrome":
            return {'major': '110', 'minor': '150', 'webkit': '537.36'}
        elif browser_type == "firefox":
            return {'major': '115', 'minor': '0'}
        elif browser_type == "edge":
            return {'major': '112', 'minor': '50', 'webkit': '537.36'}
        elif browser_type == "safari":
            return {'major': '16', 'minor': '3', 'webkit': '605.1.15'}
        return {}

    def _get_mock_user_agents(self, browser_type):
        if browser_type == "chrome":
            return Chrome().user_agents()
        elif browser_type == "firefox":
            return Firefox().user_agents()
        elif browser_type == "edge":
            return Edge().user_agents()
        elif browser_type == "safari":
            return Safari().user_agents()
        return {}

    def test_singleton_behavior(self):
        user_agent1 = UserAgent(platform_type="desktop", device_type="windows", browser_type="chrome")
        user_agent2 = UserAgent(platform_type="desktop", device_type="windows", browser_type="chrome")
        self.assertEqual(id(user_agent1), id(user_agent2))

        user_agent3 = UserAgent(platform_type="mobile", device_type="android", browser_type="chrome")
        self.assertNotEqual(id(user_agent1), id(user_agent3))

if __name__ == '__main__':

    # Obeject testing
    # TestUserAgent
    user_agent = UserAgent(platform_type="desktop", device_type="windows", browser_type="chrome")
    print("----------------------------------")
    print("1: ",  id(user_agent))
    print("1: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop", device_type="windows", browser_type="chrome")
    print("----------------------------------")
    print("1: ",  id(user_agent))
    print("1: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop", device_type="windows", browser_type="edge")
    print("\n2: ", id(user_agent))
    print("2: ", user_agent.generate())
    print("2: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop", device_type="windows", browser_type="edge")
    print("\n2: ", id(user_agent))
    print("2: ", user_agent.generate())
    print("2: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop", device_type="windows", browser_type="firefox")
    print("\n3: ", id(user_agent))
    print("3: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop", device_type="windows", browser_type="firefox")
    print("\n3: ", id(user_agent))
    print("3: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop", device_type="linux", browser_type="chrome")
    print("\n4: ", id(user_agent))
    print("4: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop", device_type="linux", browser_type="chrome")
    print("\n4: ", id(user_agent))
    print("4: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop", device_type="linux", browser_type="edge")
    print("\n5: ", id(user_agent))
    print("5: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop", device_type="linux", browser_type="edge")
    print("\n5: ", id(user_agent))
    print("5: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop", device_type="linux", browser_type="firefox")
    print("\n6: ", id(user_agent))
    print("6: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop", device_type="linux", browser_type="firefox")
    print("\n6: ", id(user_agent))
    print("6: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile", device_type="android", browser_type="chrome")
    print("\n7: ", id(user_agent))
    print("7: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile", device_type="android", browser_type="chrome")
    print("\n7: ", id(user_agent))
    print("7: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile", device_type="android", browser_type="edge")
    print("\n8 ID: ", id(user_agent))
    print("8: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile", device_type="android", browser_type="edge")
    print("\n8 ID: ", id(user_agent))
    print("8: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile", device_type="android", browser_type="firefox")
    print("\n9 ID: ", id(user_agent))
    print("9: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile", device_type="android", browser_type="firefox")
    print("\n9 ID: ", id(user_agent))
    print("9: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop", device_type="macos", browser_type="chrome")
    print("\n10 ID: ", id(user_agent))
    print("10: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop", device_type="macos", browser_type="chrome")
    print("\n10 ID: ", id(user_agent))
    print("10: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop", device_type="macos", browser_type="edge")
    print("\n11 ID: ", id(user_agent))
    print("11: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop", device_type="macos", browser_type="edge")
    print("\n11 ID: ", id(user_agent))
    print("11: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop", device_type="macos", browser_type="safari")
    print("\n12 ID: ", id(user_agent))
    print("12: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop", device_type="macos", browser_type="safari")
    print("\n12 ID: ", id(user_agent))
    print("12: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop", device_type="macos", browser_type="firefox")
    print("\n13 ID: ", id(user_agent))
    print("13: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="desktop", device_type="macos", browser_type="firefox")
    print("\n13 ID: ", id(user_agent))
    print("13: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile", device_type="ios", browser_type="chrome")
    print("\n14 ID: ", id(user_agent))
    print("14: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile", device_type="ios", browser_type="chrome")
    print("\n14 ID: ", id(user_agent))
    print("14: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile", device_type="ios", browser_type="edge")
    print("\n15 ID: ", id(user_agent))
    print("15: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile", device_type="ios", browser_type="edge")
    print("\n15 ID: ", id(user_agent))
    print("15: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile", device_type="ios", browser_type="safari")
    print("\n16 ID: ", id(user_agent))
    print("16: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile", device_type="ios", browser_type="safari")
    print("\n16 ID: ", id(user_agent))
    print("16: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile", device_type="ios", browser_type="firefox")
    print("\n17 ID: ", id(user_agent))
    print("17: ", user_agent.generate())
    print("----------------------------------")
    user_agent = UserAgent(platform_type="mobile", device_type="ios", browser_type="firefox")
    print("\n17 ID: ", id(user_agent))
    print("17: ", user_agent.generate())
    print("----------------------------------")
    
    # Unit testing
    unittest.main()