from abc import ABC, abstractmethod


class Messager(ABC):
    def __init__(self,title):
        self.title = title

    @abstractmethod
    def get_message(self):
        pass

    @abstractmethod
    def send_message(self):
        pass