import threading
from typing import Any, Dict, Tuple

class Singleton(type):
    """
    A metaclass that implements the Singleton pattern.
    Allows multiple instances if they are created with different constructor arguments.
    """
    
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls._instances: Dict[Tuple[Any, ...], Any] = {}
        cls._lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        """
        Overrides the default class instantiation method.
        Creates a new instance if no matching instance exists, otherwise returns the existing one.
        """
        key = (cls, args, frozenset(kwargs.items()))
        with cls._lock:
            if key not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[key] = instance
        return cls._instances[key]