
from downedit.service.client import Client


class BaseDownloader(Client):
    """
    Base class for downloading files.
    """

    def __init__(self, kwargs: dict = ...):
        super().__init__()
        pass