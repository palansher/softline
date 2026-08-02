from TemplatePage import TemplatePage


class CommonPage(TemplatePage):
    def content(self):
        print(f"Страница для сайта\nНазвание страницы: {self.title}: {self.description}")