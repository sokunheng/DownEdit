from random import choice
from .user_agents import UserAgent
from .serialization import (
    format_mm_version,
    major_version,
    ch_bool,
    ch_string,
    ch_brand_list
)

class ClientHints:
    """
    The ClientHints class.

    Description:
        The ClientHints class generates the Client Hints for the UserAgent object.

    Args:
        user_agent (UserAgent): The UserAgent object.

    References:
        https://wicg.github.io/ua-client-hints/#http-ua-hints
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA
    """
    mobile: str
    platform: str
    platform_version: str
    brands: str
    brands_full_version_list: str
    bitness: str
    architecture: str
    model: str
    wow64: str

    def __init__(self, user_agent: UserAgent):
        self.__user_agent = user_agent
        self.__cache = {}

    def __getattr__(self, name):
        """
        __getattr__ method.

        Args:
            name (_type_): The name of the attribute.

        Returns:
            _type_: The value of the attribute.
        """
        if name in self.__cache:
            return self.__cache[name]

        hint_methods = {
            'mobile'                   : lambda: ch_bool(self.get_mobile()),
            'platform'                 : lambda: ch_string(self.get_platform()),
            'platform_version'         : lambda: ch_string(self.get_platform_version()),
            'brands'                   : lambda: ch_brand_list(self.get_brands()),
            'brands_full_version_list' : lambda: ch_brand_list(self.get_brands(full_version_list=True)),
            'bitness'                  : lambda: ch_string(self.get_bitness()),
            'architecture'             : lambda: ch_string(self.get_architecture()),
            'model'                    : lambda: ch_string(self.get_model()),
            'wow64'                    : lambda: ch_bool(self.get_wow64()),
        }

        if name in hint_methods:
            self.__cache[name] = hint_methods[name]()
            return self.__cache[name]

    def get_mobile(self):
        return self.__user_agent.device_type in ('ios', 'android')

    def get_platform(self):
        platform_map = {
            'ios'   : 'iOS',
            'macos' : 'macOS'
        }
        return platform_map.get(
            self.__user_agent.device_type,
            self.__user_agent.device_type.title()
        )

    def get_platform_version(self):
        if self.__user_agent.device_type == 'windows' and major_version(self.__user_agent.platform_version) == '10':
            return choice(['10.0.0', '13.0.0'])
        return format_mm_version(self.__user_agent.platform_version)

    def get_brands(self, full_version_list=False):
        brand_map = {
            'chrome': ['Google Chrome', 'Chromium'],
            'edge': ['Microsoft Edge', 'Chromium']
        }

        browser_brands = brand_map.get(self.__user_agent.browser_type, [])
        browser_version = self.get_browser_version(full_version=full_version_list)

        brands = [{'brand': 'Not)A;Brand', 'version': '99.0.0.0' if full_version_list else '99'}]
        for brand in browser_brands:
            brands.append({'brand': brand, 'version': browser_version})

        return brands

    def get_browser_version(self, full_version=True):
        if full_version:
            formatted_version = format_mm_version(self.__user_agent.browser_version)
            return formatted_version
        else:
            major_ver = major_version(self.__user_agent.browser_version)
            return major_ver

    def get_bitness(self):
        if self.__user_agent.device_type == 'android':
            return choice(['32', '64'])
        return '64'

    def get_architecture(self):
        if self.__user_agent.device_type in ['android', 'ios']:
            return 'arm'
        if self.__user_agent.platform_type == 'macos':
            return choice(['arm', 'x86'])
        return 'x86'

    def get_model(self):
        return getattr(self.__user_agent.platform_version, 'platform_model', '')

    def get_wow64(self):
        return self.__user_agent.platform_type == 'windows'

    def __str__(self):
        return self.brands