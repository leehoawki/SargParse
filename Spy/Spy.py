#!/usr/bin/python
import sys
import re
import SargParse


def __import_module(exp):
    matches = re.findall(r"([a-zA-Z_][a-zA-Z0-9_]*)\.", exp)
    for module_name in matches:
        try:
            module = __import__(module_name)
            globals()[module_name] = module
        except ImportError as e:
            pass


def __evaluate(exp):
    resp = eval(exp)
    __print_resp(resp)


def __apply(exp, lines):
    for line in lines:
        x = __parse(line)
        print eval(exp)


def __filter(exp, lines):
    for line in lines:
        x = __parse(line)
        resp = eval(exp)
        if resp:
            print x


def __reduce(exp, lines):
    y = None
    for line in lines:
        if y:
            x = __parse(line)
            y = eval(exp)
        else:
            y = __parse(line)
    if y:
        print y


def __lisp(exp, lines):
    x = map(__parse, list(lines))
    resp = eval(exp)
    __print_resp(resp)


def __print_resp(resp):
    if isinstance(resp, list):
        for o in resp:
            print o
    else:
        print resp


def __parse(line):
    return line[0:-1] if line[-1] == '\n' else line

if __name__ == '__main__':
    parser = SargParse.SargParser()

    group = SargParse.GroupArgument()
    group.add_argument('-x', message='execute lambda expression using standard input as x')
    group.add_argument('-f', message='filter the standard input using a lambda expression')
    group.add_argument('-r', message='reduce the standard input using expression of x and y')
    group.add_argument('-l', message='apply the expression to the standard input as a list')

    parser.add_group_argument(group)
    parser.add_argument('exp', message="the expression to execute")
    namespace = parser.parse_arg()
    __import_module(namespace.exp)
    if namespace.x:
        __apply(namespace.exp, sys.stdin)
    elif namespace.f:
        __filter(namespace.exp, sys.stdin)
    elif namespace.r:
        __reduce(namespace.exp, sys.stdin)
    elif namespace.l:
        __lisp(namespace.exp, sys.stdin)
    else:
        __evaluate(namespace.exp)
