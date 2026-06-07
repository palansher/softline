#3.1
for i in range(2,10):
    for j in range(2,6):
        str=f"{j} x {i} = {i*j}"
        print (str, end=f"{" "*(10-len(str))}   ")
    print()

#3.2
from math import sqrt
print ("Простые числа: ", end="")
for n in range(2,101):
    i = 2
    while i <= sqrt(n):
        if n % i == 0:
            break
        i += 1
    else:
        print(n, end=" ")