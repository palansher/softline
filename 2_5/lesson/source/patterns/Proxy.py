from abc import ABC, abstractmethod



class RealObect(ABC):
    @abstractmethod
    def add_data_to_db(self):
        pass

class RealObectMainFinish(RealObect):
    def add_data_to_db(self):
        print('Отправка данных в базу')

class RealObectMain:
    def add_data_to_db(self):
        print('Выполняем проверку данных до вызова основного метода')
        RealObectMainFinish().add_data_to_db()

client = RealObectMain()
client.add_data_to_db()