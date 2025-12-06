from abc import ABC, abstractmethod


class BaseResolver(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def get_ip(self) -> str:
        pass
