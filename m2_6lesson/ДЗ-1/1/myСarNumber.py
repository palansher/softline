class CarNumber:
    def __init__(self, series, number, region, owner_fio):
        self.series = series
        self.number = number
        self.region = region
        self.owner_fio = owner_fio

    def __str__(self):
        return f"{self.series[0]}{self.number}{self.series[1:]}{self.region} : {self.owner_fio}"
