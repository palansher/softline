import csv


# def read_csv(file_name):
#     with open(file_name,'r',encoding='utf-8') as f:
#         data = f.readlines()



def read_file(filename):
    with open(filename,'r',encoding='utf-8') as f:
        for line in f:
            yield line

gen = read_file('men.csv')
print(next(gen))
print(next(gen))
