"""Base class for DNS updater drivers in dnswatch.

All updater drivers must inherit from this class and implement the
get_current_ip() and update() methods.
"""

from abc import ABC, abstractmethod


class BaseUpdater(ABC):
    """Abstract base class for all updater implementations."""

    def __init__(self, config):
        self.config = config

    @abstractmethod
    def get_current_ip(self) -> str:
        """Return the IP currently set in the DNS provider."""
        pass

    @abstractmethod
    def update(self, ip: str):
        """Push the given IP to the DNS provider."""
        pass
