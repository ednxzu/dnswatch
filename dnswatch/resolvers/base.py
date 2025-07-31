"""Base class for DNSWatch resolver drivers.

All resolvers must inherit from BaseResolver and implement the get_ip() method.
"""

from abc import ABC, abstractmethod


class BaseResolver(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def get_ip(self) -> str:
        """Return the current public IP address as a string."""
        pass
