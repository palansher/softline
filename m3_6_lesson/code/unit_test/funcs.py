def get_sum(a,b):
    return a+b

def get_mult(a,b):
    return a*b

def get_div(a,b):
    if b == 0:
        raise ValueError('division by zero')

    return a/b