
from downedit.service.client import Client
from downedit.utils import (
    console,
    column
)


class BaseDownloader(Client):
    """
    Base class for downloading files.
    """

    def __init__(self, kwargs: dict = ...):
        super().__init__()

        self.progress = console().progress_bar(
            column_config=column().download()
        )

        pass