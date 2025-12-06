from abc import ABC, abstractmethod


class BaseUpdater(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def get_current_ip(self) -> str | None:
        pass

    @abstractmethod
    def update(self, ip: str):
        pass
