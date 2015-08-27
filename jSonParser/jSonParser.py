class MyObject(object):
    def __init__(self):
        self.__str__ = self.__repr__


class JObject(MyObject):
    def __init__(self, o):
        MyObject.__init__(self)
        self.o = o

    def __repr__(self):
        ol = map(lambda x: str(x[0]) + ":" + str(x[1]), self.o)
        return "{" + ",".join(ol) + "}"


class JArray(MyObject):
    def __init__(self, l):
        MyObject.__init__(self)
        self.l = l

    def __repr__(self):
        return "[" + ",".join(map(str, self.l)) + "]"


class JString(MyObject):
    def __init__(self, a):
        MyObject.__init__(self)
        self.a = a

    def __repr__(self):
        return '"' + self.a + '"'


class JNumber(MyObject):
    def __init__(self, n):
        MyObject.__init__(self)
        self.n = n

    def __repr__(self):
        return str(self.n)


class JBool(MyObject):
    def __init__(self, b):
        MyObject.__init__(self)
        self.b = b

    def __repr__(self):
        if self.b:
            return "true"
        return "false"


class JNull(MyObject):
    def __init__(self):
        MyObject.__init__(self)

    def __repr__(self):
        return "null"


def load(s):
    s = trim(s)
    if len(s) == 0:
        raise Exception("empty string.")

    if s[0] == "{":
        o = parse_obj(s)
        return o[0]
    elif s[0] == "[":
        a = parse_array(s)
        return a[0]
    else:
        raise Exception("parse error:" + s)


def trim(s):
    """
    trim the whitespaces in the head
    >>> trim(" ")
    ''
    >>> trim(" a")
    'a'
    >>> trim("    a  b")
    'a  b'
    """
    index = 0
    whites = " \r\n"
    while index < len(s) and s[index] in whites:
        index += 1
    return s[index:]


def parse_obj(s):
    """
    parse object from the header of the input
    >>> parse_obj('{"1":true}')
    ({"1":true}, '')
    >>> parse_obj('{"1":true, "wa":[1,2,3,4]}')
    ({"1":true,"wa":[1.0,2.0,3.0,4.0]}, '')
    >>> parse_obj('{"name":"test","age":"18"}')
    ({"name":"test","age":"18"}, '')
    >>> parse_obj('{"people":null}')
    ({"people":null}, '')
    """
    s = trim(s[1:])
    if s[0] == "}":
        return JObject([]), s[1:]
    l = []
    while True:
        if s[0] != '"':
            raise Exception('expecting a "')
        key, s = parse_string(s)
        s = trim(s)
        if s[0] != ':':
            raise Exception('expecting a :')
        s = trim(s[1:])
        val, s = parse_value(s)
        s = trim(s)
        l.append((key, val))
        if s[0] == ',':
            s = trim(s[1:])
        elif s[0] == '}':
            return JObject(l), s[1:]
        else:
            raise Exception('expecting a , or }')


def parse_array(s):
    """
    parse array from the header of the input
    >>> parse_array('[1,\"w]a\"]haha')
    ([1.0,"w]a"], 'haha')
    >>> parse_array("[1, true]")
    ([1.0,true], '')
    >>> parse_array("[1, true  ]")
    ([1.0,true], '')
    """
    s = trim(s[1:])
    if s[0] == "]":
        return JArray([]), s[1:]
    a = []
    while True:
        val, s = parse_value(s)
        a.append(val)
        s = trim(s)
        if s[0] == ',':
            s = trim(s[1:])
        elif s[0] == ']':
            return JArray(a), s[1:]
        else:
            raise Exception('expecting a , or ]')


def parse_string(s):
    """
    parse string from the header of the input
    >>> parse_string('\"wa\"haha')
    ("wa", 'haha')
    >>> parse_string('\"w\\\\\\"a\"haha')
    ("w\\\"a", 'haha')
    >>> parse_string('"wa\\\\\\\\"haha')
    ("wa\\\\", 'haha')
    """
    index = 1
    escape = False
    #while index < len(s) and ((s[index] != '"') or ((s[index] == '"') and (s[index-1] == "\\"))):
    while index < len(s):
        if escape:
            escape = False
        elif s[index] == '"':
            break
        elif s[index] == '\\':
            escape = True
        index += 1
    if index >= len(s) or s[index] != '"':
        raise Exception('expecting a "')
    return JString(s[1:index]), s[index+1:]


def parse_null(s):
    if s.startswith("null"):
        return JNull(), s[4:]
    else:
        raise Exception("failed to parse:" + s)


def parse_true(s):
    if s.startswith("true"):
        return JBool(True), s[4:]
    else:
        raise Exception("failed to parse:" + s)


def parse_false(s):
    if s.startswith("false"):
        return JBool(False), s[5:]
    else:
        raise Exception("failed to parse:" + s)


def parse_number(s):
    """
    parse number from the header of the input
    >>> parse_number("1")
    (1.0, '')
    >>> parse_number("1.0a")
    (1.0, 'a')
    >>> parse_number("1.0 a")
    (1.0, ' a')
    """
    index = 0
    ns = "1234567890-+."
    while index < len(s) and s[index] in ns:
        index += 1
    try:
        return JNumber(float(s[:index])), s[index:]
    except Exception:
        raise Exception("failed to parse:" + s)


def parse_value(s):
    if s[0] == "n":
        return parse_null(s)
    if s[0] == "t":
        return parse_true(s)
    if s[0] == "f":
        return parse_false(s)
    if s[0] == '"':
        return parse_string(s)
    if s[0] == "{":
        return parse_obj(s)
    if s[0] == "[":
        return parse_array(s)
    else:
        return parse_number(s)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
