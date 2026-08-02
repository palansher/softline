from TemplatePage import TemplatePage


class AdminPage(TemplatePage):
    def content(self):
        print(f"Страница для админки\nНазвание страницы: {self.title}: {self.description}")