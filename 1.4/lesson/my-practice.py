
sum = lambda a,b : a+b
sub = lambda a,b : a-b
mult = lambda a,b : a*b
div = lambda a,b : a/b

# operation: +|-|*|/

def my_math(a,b,operation):
    if operation == '+':
        return sum(a,b)

    if operation == '-':
        return sub(a,b)

    if operation == '*':
        return mult(a,b)

    if operation == '/':
        if b == 0:
            print("Делить на ноль нельзя")
            return
        return div(a,b)

print("sum=", my_math(2,3,'+'))
print("sub=", my_math(6,3,'-'))
print("mult=", my_math(5,5, '*'))
print("div=", my_math(5,2, '/'))
