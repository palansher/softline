from abc import ABC, abstractmethod


class Security(ABC):
    @abstractmethod
    def add_secure(self):
        pass