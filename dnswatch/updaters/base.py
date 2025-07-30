from abc import ABC, abstractmethod


class BaseUpdater(ABC):
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
