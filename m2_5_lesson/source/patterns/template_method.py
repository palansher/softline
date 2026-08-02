from abc import ABC, abstractmethod


class Education(ABC):
   def steps_to_result(self):
       self.income()
       self.learn()
       self.pass_exams()

   @abstractmethod
   def income(self):
       pass

   @abstractmethod
   def learn(self):
       pass


   def pass_exams(self):
       print("Сдаем экзамены и получаем документ об образовании")

class School(Education):
    def income(self):
        print("Поступаем без экзаменов")

    def learn(self):
        print("Посещаем уроки и делаем ДЗ")


class Univer(Education):
    def income(self):
        print("Поступаем в Универ на основе ЕГЭ")

    def learn(self):
        print("Посещаем лекции и практику и делаем ДЗ")


univer = Univer()
univer.steps_to_result()
