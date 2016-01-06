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


class IllegalArgException(SargException):
    def __init__(self, message="", *args, **kwargs):
        super(IllegalArgException, self).__init__("Illegal arguments %s." % message)


class InCompatibleArgException(SargException):
    def __init__(self, message="", *args, **kwargs):
        super(InCompatibleArgException, self).__init__("Incompatible arguments %s." % message)


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

    def get_message(self, offset):
        space = 4
        return self.name.ljust(offset + space) + self.message

    def accept(self, visitor):
        return getattr(visitor, "visit%s" % self.__class__.__name__)(self)

    @classmethod
    def create(cls, name, message, **kwargs):
        if name == "h,--help":
            return HelpArgument(name, message, **kwargs)
        elif name.split(",")[0][0] == "-":
            return OptionalArgument(name, message, **kwargs)
        else:
            return PositionalArgument(name, message, **kwargs)


class Arguments(Argument):
    def __init__(self):
        self.arguments = []

    def arguments(self):
        pass

    def append(self, argument):
        self.arguments.append(argument)

    def values(self):
        return self.arguments


class OptionalArgument(Argument):
    pass


class PositionalArgument(Argument):
    pass


class HelpArgument(Argument):
    pass


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


class Visitor(Singleton):
    def visitArguments(self, args):
        pass

    def visitOptionalArgument(self, arg):
        pass

    def visitPositionalArgument(self, arg):
        pass

    def visitHelpArgument(self, arg):
        pass


class UsageVisitor(Visitor):
    def visitArguments(self, args):
        prog = os.path.basename(sys.argv[0])
        return "Usage: %s %s" % (prog, " ".join([a.accept(self) for a in args.values()]))

    def visitOptionalArgument(self, arg):
        return "[" + arg.name + "]"

    def visitPositionalArgument(self, arg):
        return arg.name

    def visitHelpArgument(self, arg):
        return "[" + arg.name + "]"


class LengthVisitor(Visitor):
    def visitArguments(self, args):
        return max([a.accept(self) for a in args.values()])

    def visitOptionalArgument(self, arg):
        return len(arg.name)

    def visitPositionalArgument(self, arg):
        return len(arg.name)

    def visitHelpArgument(self, arg):
        return len(arg.name)


class ParseVisitor(Visitor):
    def visitArguments(self, args):
        pass

    def visitOptionalArgument(self, arg):
        pass

    def visitPositionalArgument(self, arg):
        pass

    def visitHelpArgument(self, arg):
        pass


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
        sys.exit(1)


class DebugErrorHandler(object):
    def handle(self, e):
        raise e


class SargParser(object):
    """
    >>> import SargParse
    >>> s = SargParse.SargParser()
    >>> s.add_argument('-x', message='x factor')
    >>> s.add_argument('-y', message='y factor')
    >>> s.add_argument('exp', message='expression')
    >>> s.print_help()
    Usage: docrunner.py [-h,--help] [-x] [-y] exp
    Optional:
    -h,--help    show this help message and exit.
    -x           x factor
    -y           y factor
    Positional:
    exp          expression


    >>> s = SargParse.SargParser()
    >>> group = SargParse.GroupArgument()
    >>> group.add_argument('-a', message='a factor')
    >>> group.add_argument('-b', message='b factor')
    >>> group.add_argument('-c', message='c factor')
    >>> s.add_group_argument(group)
    >>> s.add_argument('exp', message='expression')
    >>> s.print_help()
    Usage: docrunner.py [-h,--help] [-a|-b|-c] exp
    Optional:
    -h,--help    show this help message and exit.
    -a           a factor
    -b           b factor
    -c           c factor
    Positional:
    exp          expression
    """

    def __init__(self, handler=DefaultErrorHandler):
        self.optional_arg = []
        self.positional_arg = []
        self.arguments = Arguments()
        self.add_argument("-h,--help", message="show this help message and exit.", action="help")
        self.handler = handler()
        self.usage_visitor = UsageVisitor()
        self.length_visitor = LengthVisitor()

    def parse_arg(self, expression=(sys.argv)[1:]):
        try:
            return NameSpace(self.parse(expression))
        except SargException, e:
            print(self.get_usage(), file=sys.stderr)
            print(e, file=sys.stderr)
            self.handler.handle(e)

    def add_argument(self, name, message="", **kwargs):
        argument = Argument(name, message, **kwargs)
        if argument.type == "optional":
            self.optional_arg.append(argument)
        else:
            self.positional_arg.append(argument)

        self.arguments.append(Argument.create(name, message, **kwargs))

    def add_group_argument(self, group):
        self.optional_arg.append(group)

    def print_help(self):
        print(self.get_usage())
        l = self.get_arguments_length()
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
                else:
                    raise IllegalArgException(expression[0])

        namespace = parse_rest(self.positional_arg, self.optional_arg, expression, {})
        return namespace

    def get_arguments_length(self):
        return self.length_visitor.visitArguments(self.arguments)

    def get_usage(self):
        return self.usage_visitor.visitArguments(self.arguments)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
