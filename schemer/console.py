def get():
    input = raw_input('scheme>')
    if len(input) != 0 :
        return parse(tokenize(input))

def put(string):
    if string is not None:
        print string

def parse(tokens):
    t = tokens.pop(0)
    if t == '(':
        L = []
        while tokens[0] != ')':
            L.append(parse(tokens))
        tokens.pop(0)
        return L
    else:
        return atom(t)

def atom(token):
    try :
        return int(token)
    except :
        try :
            return float(token)
        except:
            return token

def tokenize(exp):
    return exp.replace(')',' ) ').replace('(',' ( ').split()


