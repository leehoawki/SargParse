def swipe(value, patterns):
    for pattern in patterns:
        p = pattern[0]
        expressions = pattern[1]
        matcher = validate(p)
        if matcher.match(value):
            locals().update(matcher.result)
            return eval(expressions)


class Matcher(object):
    result = {}

    def match(self, obj):
        raise Exception("Undefined Object " + obj)


class Wildcard(Matcher):
    def match(self, obj):
        return True


_ = Wildcard()
Swipe = swipe


class Value(Matcher):
    def __init__(self, _value):
        self._value = _value

    def match(self, obj):
        return obj == self._value


class Type(Matcher):
    def __init__(self, pattern):
        self._name = pattern.split(":")[0]
        self._type = pattern.split(":")[1]

    def match(self, obj):
        self.result[self._name] = obj
        return type(obj).__name__ == self._type


class Deconstruct(Matcher):
    def __init__(self, pattern):
        self._arguments = pattern.split(",")

    def match(self, obj):
        if type(obj) == list:
            result, kv = un_apply_list(self._arguments, obj)
        elif type(obj) == str:
            result, kv = un_apply_list(self._arguments, obj)
        else:
            result, kv = obj.decontruct(self._arguments)
        if result:
            self.result.update(kv)
        return result


def un_apply_list(arguments, l):
    if len(l) < len(arguments) -1:
        return False, None
    kv = {}
    temp = l[:]
    for arg in arguments[:-1] :
        kv[arg] = temp.pop(0)
    kv[arguments[-1]] = temp
    return True, kv

def validate(pattern):
    if type(pattern) == str and ":" in pattern:
        return Type(pattern)
    elif type(pattern) == str and "," in pattern:
        return Deconstruct(pattern)
    elif type(pattern) is int:
        return Value(pattern)
    elif type(pattern) is str:
        return Value(pattern)
    elif pattern == _:
        return _
    else:
        return Matcher()


