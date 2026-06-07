class Passport:
    def __init__(self,series,number,fio):
        self.series = series
        self.number = number
        self.fio = fio

    def __str__(self):
        return f'{self.series} {self.number} : {self.fio}'

