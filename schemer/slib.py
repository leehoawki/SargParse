def eq(*args):
    temp = args[0]
    for i in args:
        if temp != i:
            return False
        temp = i
    return True

def add(*args):
    val = 0
    for i in args:
        val += i
    return val

def sub(*args):
    val = args[0]
    for i in args[1:]:
        val -= i
    return val

def mul(*args):
    val = 1
    for i in args:
        val *= i
    return val

def div(*args):
    args = list(args)
    val = args.pop(0)
    for i in args:
        val /= i
    return val
