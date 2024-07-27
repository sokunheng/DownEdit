import random

from ..utils.singleton import Singleton
from .browsers import Browser
from .platforms import Platform

def version(version_dict, strip_zero=False):
    major = version_dict['major']
    minor = version_dict.get('minor', 0)
    
    if not strip_zero or minor > 0:
        return f"{major}.{minor}"
    
    return str(major)

class UserAgent(metaclass=Singleton):
    def __init__(
        self, 
        platform_type="desktop", 
        device_type="windows", 
        browser_type="chrome"
    ):
        self.platform_type = platform_type.lower()
        self.browser_type = browser_type.lower()
        self.device_type = device_type.lower()
        
        self.browser = Browser(self.browser_type)
        self.platform = Platform(self.platform_type, self.device_type)
        
    def __get_user_agent(self) -> str:
        """
        Generate a user agent string based on the platform, device, and browser types.
        
        Returns:
            str: A user agent string.
        """
        
        platform_version = self.platform.get_version()
        browser_version = self.browser.get_version()
        browser_user_agents = self.browser.get_user_agents()
        browser_template = random.choice(browser_user_agents.get(str(self.device_type), []))

        replacements = {
            '{windows}' : platform_version.get('major', ''),
            '{webkit}'  : browser_version.get('webkit', ''),
            '{chrome}'  : version(browser_version),
            '{edge}'    : version(browser_version), 
            '{firefox}' : version(browser_version, strip_zero=True),
            '{linux}'   : platform_version.get('major', ''),
            '{android}' : platform_version.get('major', '').replace('.0', ''),
            '{model}'   : f"; {platform_version.get('platform_model', '')}",
            '{build}'   : f"; Build/{platform_version.get('build_number', '')}",
            '{ios}'     : version(platform_version, strip_zero=True).replace('.', '_'),
            '{safari}'  : version(browser_version)
        }

        for key, value in replacements.items():
            browser_template = browser_template.replace(key, str(value))

        # Remove any remaining placeholders (e.g., if model/build not found)
        browser_template = browser_template.replace('{build}', '').replace('{model}', '') 
        
        return browser_template
    
    def generate(self) -> str:
        """
        Generate a user agent string based on the platform, device, and browser types.

        Returns:
            str: A user agent string.
        """
        return self.__get_user_agent()