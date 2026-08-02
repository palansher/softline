class Numauto:
    """Класс обьектa (номер и владелец транспортного средства)"""
    def __init__(self,series,number,region,fio):
        self.series = series
        self.number = number
        self.region = region
        self.fio = fio
        self.fullnumber = series[0]+number+series[1]+series[2]+region 

    def __str__(self):
        return f'{self.fullnumber}'

