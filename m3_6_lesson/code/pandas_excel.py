import pandas as pd

store = pd.DataFrame(
    {
        "mark":["Audi","VW","BMW"],
        "model":["A6","Golf","X5"],
        "prices":[1000,900,1200]
    }
)

store.to_excel("cars.xlsx",index=False,sheet_name="Автомобили")

# cars = pd.read_excel('cars.xlsx',usecols="A,C")
# print(cars)