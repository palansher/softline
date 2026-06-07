from messengers.Messager import Messager


class WatsUp(Messager):
    author = "Брайан Эктон"
    def get_message(self):
        print(f'Сообщение получено в мессенджере{self.title}. [Разработчик мессенджера {self.author}]')

    def send_message(self):
        print(f'Сообщение отправлено в мессенджере{self.title}. [Разработчик мессенджера {self.author}')