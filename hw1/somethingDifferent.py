x = "this prog needs to number for calculate\n"

y = "first number you insert will be the base and second one will be the exp \n"

z = 'for example you insert base as 5 and insert exp as 2 programs answer will be 25.\n'

k = 'NOTE: your base can be an floating point (for example: 0.45) but\n if you inser your ext as a floating point prog wont work\n'

print(x, y, z, k, sep='\n')



def exponansial(b, e):
    
    if b == 1:
        return 1
    
    elif b == 0:
        return 0
    
    elif e == 0:
        return 1

    elif e < 0:
        return 'please insert a possitive number'
    else:
        return b * exponansial(b, e - 1)



b = input('your base number please: ')

e = input('your exp number please: ')

try:
    c = float(b)
    d = int(e)

    print(exponansial(c, d))

except ValueError:
    print('you can only insert numbers')


