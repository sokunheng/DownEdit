import random


class Chrome():
    """
    Google Chrome
    
    Description:
        The version of Chrome is based on the WebKit version. We have used the WebKit version to determine the minor version range.
    
    Reference:
        https://chromereleases.googleblog.com/search/label/Stable%20updates
    """
    def __init__(self):
        pass
    
    def get_versions(self): 
        return  {
            '100.0.4896': {'minor_range': (0, 255), 'webkit': '537.36'},
            '101.0.4951': {'minor_range': (0, 255), 'webkit': '537.36'},
            '102.0.5005': {'minor_range': (0, 255), 'webkit': '537.36'},
            '103.0.5060': {'minor_range': (0, 255), 'webkit': '537.36'},
            '104.0.5112': {'minor_range': (0, 255), 'webkit': '537.36'},
            '105.0.5195': {'minor_range': (0, 255), 'webkit': '537.36'},
            '106.0.5249': {'minor_range': (0, 255), 'webkit': '537.36'},
            '107.0.5304': {'minor_range': (0, 255), 'webkit': '537.36'},
            '108.0.5359': {'minor_range': (0, 255), 'webkit': '537.36'},
            '109.0.5414': {'minor_range': (0, 255), 'webkit': '537.36'},
            '110.0.5481': {'minor_range': (0, 255), 'webkit': '537.36'},
            '111.0.5563': {'minor_range': (0, 255), 'webkit': '537.36'},
            '112.0.5615': {'minor_range': (0, 255), 'webkit': '537.36'},
            '114.0.5735': {'minor_range': (0, 255), 'webkit': '537.36'},
            '115.0.5790': {'minor_range': (0, 255), 'webkit': '537.36'},
            '116.0.5845': {'minor_range': (0, 255), 'webkit': '537.36'},
            '117.0.5938': {'minor_range': (0, 255), 'webkit': '537.36'},
            '118.0.5993': {'minor_range': (0, 255), 'webkit': '537.36'},
            '119.0.6045': {'minor_range': (0, 255), 'webkit': '537.36'},
            '120.0.6099': {'minor_range': (0, 255), 'webkit': '537.36'},
            '121.0.6167': {'minor_range': (0, 255), 'webkit': '537.36'},
            '122.0.6261': {'minor_range': (0, 255), 'webkit': '537.36'},
            '123.0.6312': {'minor_range': (0, 255), 'webkit': '537.36'},
            '124.0.6367': {'minor_range': (0, 255), 'webkit': '537.36'},
            '125.0.6422': {'minor_range': (0, 255), 'webkit': '537.36'},
            '126.0.6478': {'minor_range': (0, 255), 'webkit': '537.36'},
            '127.0.6533': {'minor_range': (0, 255), 'webkit': '537.36'},
        }

class Firefox():
    """
    Mozilla Firefox
    
    description:
        The version of Firefox is based on the Gecko version. We have used the stable release version provided by Mozilla to determine the minor version range.
    
    Reference:
        https://www.mozilla.org/en-US/firefox/releases/
    """
    def __init__(self):
        pass
    
    def get_versions(self): 
        return {
            '103.0': {'minor_range': (0, 2)},
            '104.0': {'minor_range': (0, 2)},
            '105.0': {'minor_range': (0, 3)},
            '106.0': {'minor_range': (0, 5)},
            '107.0': {'minor_range': (0, 1)},
            '108.0': {'minor_range': (0, 2)},
            '109.0': {'minor_range': (0, 1)},
            '110.0': {'minor_range': (0, 1)},
            '111.0': {'minor_range': (0, 1)},
            '112.0': {'minor_range': (0, 2)},
            '113.0': {'minor_range': (0, 2)},
            '114.0': {'minor_range': (0, 2)},
            '115.0': {'minor_range': (0, 3)},
            '115.1': {'minor_range': (0, 0)},
            '115.2': {'minor_range': (0, 1)},
            '115.3': {'minor_range': (0, 1)},
            '115.4': {'minor_range': (0, 0)},
            '115.5': {'minor_range': (0, 0)},
            '115.6': {'minor_range': (0, 0)},
            '115.7': {'minor_range': (0, 0)},
            '115.8': {'minor_range': (0, 0)},
            '116.0': {'minor_range': (0, 3)},
            '117.0': {'minor_range': (0, 1)},
            '118.0': {'minor_range': (0, 2)},
            '119.0': {'minor_range': (0, 1)},
            '120.0': {'minor_range': (0, 1)},
            '121.0': {'minor_range': (0, 1)},
            '122.0': {'minor_range': (0, 1)},
            '123.0': {'minor_range': (0, 1)},
            '124.0': {'minor_range': (0, 2)},
            '125.0': {'minor_range': (1, 3)},
            '126.0': {'minor_range': (0, 0)},
            '127.0': {'minor_range': (0, 2)},
            '128.0': {'minor_range': (0, 2)},
        }

class Edge():
    """
    Microsoft Edge
    
    description:
        The version of Edge is based on the WebKit version. We have used the WebKit version to determine the minor version range.
    
    Reference:
        https://docs.microsoft.com/en-us/deployedge/microsoft-edge-release-schedule
    """
    def __init__(self):
        pass
    
    def get_versions(self): 
        return {
            '100.0.1185': {'minor_range': (0, 99), 'webkit': '537.36'},
            '101.0.1210': {'minor_range': (0, 99), 'webkit': '537.36'},
            '102.0.1245': {'minor_range': (0, 99), 'webkit': '537.36'},
            '103.0.1264': {'minor_range': (0, 99), 'webkit': '537.36'},
            '104.0.1293': {'minor_range': (0, 99), 'webkit': '537.36'},
            '105.0.1343': {'minor_range': (0, 99), 'webkit': '537.36'},
            '106.0.1370': {'minor_range': (0, 99), 'webkit': '537.36'},
            '107.0.1418': {'minor_range': (0, 99), 'webkit': '537.36'},
            '108.0.1462': {'minor_range': (0, 99), 'webkit': '537.36'},
            '109.0.1518': {'minor_range': (0, 99), 'webkit': '537.36'},
            '110.0.1587': {'minor_range': (0, 99), 'webkit': '537.36'},
            '111.0.1661': {'minor_range': (0, 99), 'webkit': '537.36'},
            '112.0.1722': {'minor_range': (0, 99), 'webkit': '537.36'},
            '113.0.1774': {'minor_range': (0, 99), 'webkit': '537.36'},
            '114.0.1823': {'minor_range': (0, 99), 'webkit': '537.36'},
            '115.0.1901': {'minor_range': (0, 99), 'webkit': '537.36'},
            '116.0.1938': {'minor_range': (0, 99), 'webkit': '537.36'},
            '117.0.2045': {'minor_range': (0, 99), 'webkit': '537.36'},
            '118.0.2088': {'minor_range': (0, 99), 'webkit': '537.36'},
            '119.0.2151': {'minor_range': (0, 99), 'webkit': '537.36'},
            '120.0.2210': {'minor_range': (0, 99), 'webkit': '537.36'},
            '121.0.2277': {'minor_range': (0, 99), 'webkit': '537.36'},
            '122.0.2365': {'minor_range': (0, 99), 'webkit': '537.36'},
            '123.0.2420': {'minor_range': (0, 99), 'webkit': '537.36'},
            '124.0.2478': {'minor_range': (0, 99), 'webkit': '537.36'},
            '125.0.2535': {'minor_range': (0, 99), 'webkit': '537.36'},
            '126.0.2592': {'minor_range': (0, 99), 'webkit': '537.36'},
            '127.0.2651': {'minor_range': (0, 99), 'webkit': '537.36'},
        }

class Safari():
    """
    Apple Safari
    
    description:
        The version of Safari is based on the WebKit version. We have used the WebKit version to determine the minor version range.
    
    Reference:
        https://developer.apple.com/documentation/safari-release-notes
    """
    def __init__(self):
        pass
    
    def get_versions(self): 
        return {
            '10': {'minor_range': (0, 0), 'webkit': '602.4.8'},
            '11': {'minor_range': (0, 0), 'webkit': '604.1.38'},
            '12': {'minor_range': (0, 1), 'webkit': '605.1.15'},
            '13': {'minor_range': (0, 1), 'webkit': '605.1.15'},
            '14': {'minor_range': (0, 1), 'webkit': '605.1.15'},
            '15': {'minor_range': (0, 6), 'webkit': '605.1.15'},
            '16': {'minor_range': (0, 6), 'webkit': '605.1.15'},
            '17': {'minor_range': (0, 6), 'webkit': '605.1.15'},
        }
    
class Browser():
    def __init__(self, browser=None):
        self.browser = self.get_browser(browser)
    
    def get_browser(self, browser_name):
        if browser_name.lower() == 'chrome':
            return Chrome()
        elif browser_name.lower() == 'firefox':
            return Firefox()
        elif browser_name.lower() == 'edge':
            return Edge()
        elif browser_name.lower() == 'safari':
            return Safari()
        else:
            return Chrome()
    
    def get_version(self):
        versions = self.browser.get_versions()
        major_version = random.choice(list(versions.keys()))
        properties = versions[major_version]
            
        __version = {}
        if major_version:
            __version["major"] = major_version
        if "minor_range" in properties:
            __version["minor"] = random.randint(*map(int, properties['minor_range']))
        if "webkit" in properties:
            __version["webkit"] = properties['webkit']
        return __version