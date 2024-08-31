class Proxy:
    """
    A class to manage and resolve proxy settings.
    """

    def __init__(self, proxies: dict = None):
        """
        Initializes the Proxy class with the given proxies.

        Args:
            proxies (dict): A dictionary of proxy settings.
        """

        self.proxies = proxies or {"all://": None}

    def get_proxy(self, scheme: str) -> str:
        """
        Retrieves the proxy URL based on the given scheme.

        Args:
            scheme (str): The scheme of the URL ('http', 'https', or 'all').

        Returns:
            str: The proxy URL or None if no proxy is set.
        """
        return self.proxies.get(f"{scheme}://") or self.proxies.get("all://")

    def set_proxies(self, proxies: dict) -> None:
        """
        Sets or updates the proxy settings.

        Args:
            proxies (dict): A dictionary of proxy settings.
        """
        self.proxies = proxies
