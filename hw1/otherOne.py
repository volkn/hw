x = 'this prog takes a number from you and then use it for powering for 2'

y = "i'm sorry for my english"

z = 'Now please inseret the number: '

k = "NOTE: this prog can only work when given number is an integer"

print(x, y, k, sep="\n")


def forse_is_with_you(a):
    
    if a == 0:
        return 1
    
    else:
        return 2 * forse_is_with_you(a - 1)



a = input(z)

try:
    thing = int(a)
    print(forse_is_with_you(thing))
except:
    print('please insert an integer')

