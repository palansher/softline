import jwt

encoded = jwt.encode({'role':'admin'},'secret_key',algorithm='HS256')
print(encoded)
print(jwt.decode(encoded,'secret_key',algorithms=['HS256']))