from __future__ import print_function
import sys
import os


class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, "_instance"):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


class SargException(Exception):
    pass


class NotEnoughArgException(SargException):
    def __init__(self, message="", *args, **kwargs):
        super(NotEnoughArgException, self).__init__("Not enough arguments %s." % message)


class TooManyArgException(SargException):
    def __init__(self, message="", *args, **kwargs):
        super(TooManyArgException, self).__init__("Too many arguments %s." % message)


class IllegalArgException(SargException):
    def __init__(self, message="", *args, **kwargs):
        super(IllegalArgException, self).__init__("Illegal arguments %s." % message)


class InCompatibleArgException(SargException):
    def __init__(self, message="", *args, **kwargs):
        super(InCompatibleArgException, self).__init__("Incompatible arguments %s." % message)


class Action(Singleton):
    pass


class _HelpAction(Action):
    def __call__(self, name, expression, parser, namespace):
        for n in name.split(","):
            if n == expression:
                parser.print_help()
                sys.exit(0)


class _StoreAction(Action):
    def __call__(self, name, expression, parser, namespace):
        namespace[name.strip("-")] = expression
        return True


class _StoreTrueAction(Action):
    def __call__(self, name, expression, parser, namespace):
        for n in name.split(","):
            if n == expression:
                namespace[name.strip("-")] = True
                return True
        return False


ACTION_MAPPING = {"help": _HelpAction(),
                  "store": _StoreAction(),
                  "storeTrue": _StoreTrueAction()}


class Argument(object):
    def __init__(self, name, message, **kwargs):
        self.name = name
        self.message = message
        if self.name.split(",")[0][0] == "-":
            self.type = "optional"
            self.action = "storeTrue"
        else:
            self.type = "positional"
            self.action = "store"
        self.__dict__.update(kwargs)

    def __call__(self, expression, parser, namespace):
        return ACTION_MAPPING[self.action](self.name, expression, parser, namespace)

    def get_name(self):
        if self.type == "optional":
            return "[" + self.name + "]"
        return self.name

    def get_length(self):
        return len(self.name)

    def get_message(self, offset):
        space = 4
        return self.name.ljust(offset + space) + self.message


class GroupArgument(Argument):
    def __init__(self):
        self.arguments = []

    def __call__(self, expression, parser, namespace):
        for argument in self.arguments:
            if argument(expression, parser, namespace):
                return True
        return False

    def add_argument(self, name, message=""):
        argument = Argument(name, message, type="optional")
        self.arguments.append(argument)

    def get_name(self):
        return "[" + "|".join([x.name for x in self.arguments]) + "]"

    def get_length(self):
        return max(map(lambda x: len(x.name), self.arguments))

    def get_message(self, offset):
        messages = []
        for argument in self.arguments:
            messages.append(argument.get_message(offset))
        return "\n".join(messages)


class NameSpace(object):
    def __init__(self, attributes):
        self.__dict__.update(attributes)

    def __getattr__(self, name):
        try:
            o = object.__getattribute__(self, name)
            return o
        except Exception, e:
            return None


class DefaultErrorHandler(object):
    def handle(self, e):
        print(self.get_usage(), file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)


class SargParser(object):
    def __init__(self, handler=DefaultErrorHandler):
        self.prog = os.path.basename(sys.argv[0])
        self.optional_arg = []
        self.positional_arg = []
        self.add_argument("-h,--help", message="show this help message and exit.", action="help")
        self.handler = handler()

    def get_usage(self):
        return "Usage: %s %s" % (self.prog, self.get_arguments())

    def parse_arg(self, expression=sys.argv[1:]):
        try:
            return NameSpace(self.parse(expression))
        except SargException, e:
            self.handler.handle(e)

    def add_argument(self, name, message="", **kwargs):
        argument = Argument(name, message, **kwargs)
        if argument.type == "optional":
            self.optional_arg.append(argument)
        else:
            self.positional_arg.append(argument)

    def add_group_argument(self, group):
        self.optional_arg.append(group)

    def print_help(self):
        print(self.get_usage())
        l = self.max_argument_length()
        print
        print("Optional:")
        for oa in self.optional_arg:
            print(oa.get_message(l))
        print
        print("Positional:")
        for pa in self.positional_arg:
            print(pa.get_message(l))

    def parse(self, expression):
        def parse_rest(positional_arguments, optional_arguments, expression, namespace):
            if len(expression) == 0 and len(positional_arguments) == 0:
                return namespace
            elif len(expression) == 0 and len(positional_arguments) > 0:
                raise NotEnoughArgException()
            else:
                for argument in optional_arguments:
                    if argument(expression[0], self, namespace):
                        return parse_rest(positional_arguments, [a for a in optional_arguments if a != argument],
                                          expression[1:], namespace)
                if len(positional_arguments) == 0:
                    raise IllegalArgException(expression[0])
                elif positional_arguments[0](expression[0], self, namespace):
                    return parse_rest(positional_arguments[1:], optional_arguments, expression[1:], namespace)

        namespace = parse_rest(self.positional_arg, self.optional_arg, expression, {})
        return namespace

    def max_argument_length(self):
        return max(map(lambda x: x.get_length(), self.optional_arg + self.positional_arg))

    def get_arguments(self):
        return " ".join([x.get_name() for x in self.optional_arg + self.positional_arg])
