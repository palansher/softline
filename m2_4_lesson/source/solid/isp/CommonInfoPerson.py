from abc import ABC, abstractmethod


class InfoPerson(ABC):
    @abstractmethod
    def get_common_info(self):
        pass

class WorkInfo(ABC):
    @abstractmethod
    def get_work_info(self):
        pass

class SeniorDeveloper(InfoPerson, WorkInfo):
    def get_common_info(self):
        print('Общая информация о разработчике')

    def get_work_info(self):
        print('Общая информация о должностной инструкции')

class Student(InfoPerson):
    def get_common_info(self):
        print('Общая информация о студенте')

