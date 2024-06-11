import asyncio
import signal
import sys

from .singleton import Singleton

class Observer(metaclass=Singleton):
    def __init__(self):
        self._terminate_event = asyncio.Event()

    @property
    def terminate_event(self):
        """
        rovides read-only access to terminate_event
        """
        return self._terminate_event

    def _termination_received(self, signum, frame):
        """
        Internal handling of received signal
        """
        self._terminate_event.set()
        for task in asyncio.all_tasks():
            task.cancel()

        sys.exit(0)

    def register_termination_handlers(self):
        """
        Registers handlers for SIGINT and SIGTERM signals
        """
        signal.signal(signal.SIGINT, self._termination_received)
        signal.signal(signal.SIGTERM, self._termination_received)

    @classmethod
    def is_termination_signaled(cls):
        """
        Checks if termination event has been set
        """
        return cls().terminate_event.is_set()