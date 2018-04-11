x = "this prog needs to number for calculate"

y = "first number you insert will be the base and second one will be the exp "

z = 'for example you insert base as 5 and insert exp as 2 programs answer will be 25.'



print(x, y, z, sep='\n')



def exponansial(b, e):
    
    if b == 1:
        return 1
    
    elif b == 0:
        return 0
    
    elif e == 0:
        return 1

    else: 
        return b * exponansial(b, e - 1)



b = input('your base number please: ')

e = input('your exp number please: ')

try:
    c = int(b)
    d = int(e)

    print(exponansial(c, d))

except ValueError:
    print('you can only insert numbers')


