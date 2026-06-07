from abc import ABC, abstractmethod


class TemplatePage(ABC):
    def __init__(self, title,description):
        self.title = title
        self.description = description

    def header(self):
        print("Блок: Шапка сайта")

    def footer(self):
        print("Блок: Подвал сайта")

    @abstractmethod
    def content(self):
        pass

    def render(self):
        self.header()
        self.content()
        self.footer()
        print("*" * 50)