from messengers.Messager import Messager
from messengers.Security import Security


class Telegram(Messager,Security):
    author = "Российский автор"
    def get_message(self):
        self.add_secure()
        print(f'Сообщение получено в мессенджере{self.title}. [Разработчик мессенджера {self.author}]')

    def send_message(self):
        self.add_secure()
        print(f'Сообщение отправлено в мессенджере{self.title}. [Разработчик мессенджера {self.author}')

    def add_secure(self):
        print("Добавлено шифрование данных")

