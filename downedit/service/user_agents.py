import random

from ..utils.singleton import Singleton
from .browsers import Browser
from .platforms import Platform
from .serialization import format_mm_version

class UserAgent():
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

        self.generated = self.__generate()

        self.platform_version: dict
        self.browser_version: dict

    def __generate(self) -> str:
        """
        Generate a user agent string based on the platform, device, and browser types.

        Returns:
            str: A user agent string.
        """
        self.platform_version = self.platform.get_version()
        self.browser_version = self.browser.get_version()

        browser_ua = self.browser.get_user_agents()
        browser_template = random.choice(
            browser_ua.get(str(self.device_type), [])
        )

        replacements = {
            '{windows}' : self.platform_version.get('major', ''),
            '{webkit}'  : self.browser_version.get('webkit', ''),
            '{chrome}'  : format_mm_version(self.browser_version),
            '{edge}'    : format_mm_version(self.browser_version),
            '{firefox}' : format_mm_version(self.browser_version, strip_zero=True),
            '{linux}'   : self.platform_version.get('major', ''),
            '{android}' : self.platform_version.get('major', '').replace('.0', ''),
            '{model}'   : f"; {self.platform_version.get('platform_model', '')}",
            '{build}'   : f"; Build/{self.platform_version.get('build_number', '')}",
            '{ios}'     : format_mm_version(self.platform_version, strip_zero=True).replace('.', '_'),
            '{safari}'  : format_mm_version(self.browser_version)
        }

        for key, value in replacements.items():
            browser_template = browser_template.replace(key, str(value))

        # Remove any remaining placeholders (e.g., if model/build not found)
        browser_template = browser_template.replace('{build}', '').replace('{model}', '')

        return browser_template

    def __str__(self) -> str:
        return self.generated