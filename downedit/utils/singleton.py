import threading
from typing import Any, Dict, Tuple

class Singleton(type):
    """
    A metaclass that implements the Singleton pattern.
    Allows multiple instances if they are created with different constructor arguments.
    """

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls._inst_cache: Dict[Tuple[Any, ...], Any] = {}
        cls._inst_lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        """
        Overrides the default class instantiation method.
        Creates a new instance if no matching instance exists, otherwise returns the existing one.
        """
        inst_key = (cls, args, frozenset(kwargs.items()))
        with cls._inst_lock:
            if inst_key not in cls._inst_cache:
                instance = super().__call__(*args, **kwargs)
                cls._inst_cache[inst_key] = instance
        return cls._inst_cache[inst_key]