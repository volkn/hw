x = 'insert the number that you want to find its factorial: '

a = input(x)

def factorial(a):
    
    if a == 0:
        return 1
    
    elif a >= 1:
        return a * factorial(a - 1)

    else:
        return 'please insert a possitive number'

try:
    a = int(a)
    print(factorial(a))

except:
    print('please insert just a number')


