x = 'insert the number that you want to find its factorial: '

a = int(input(x))

def factorial(a):
    if a == 0:
        return 1
    else:
        return a * factorial(a - 1)

print(factorial(a))

