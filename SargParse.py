from __future__ import print_function
import sys
import os


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


class HelpException(SargException):
    pass


class ArgumentError(SargException):
    def __init__(self, message="", *args, **kwargs):
        super(ArgumentError, self).__init__("Argument error %s." % message)


class Argument(object):
    def __init__(self, name, message, **kwargs):
        self.name = name
        self.message = message

    def accept(self, visitor):
        return getattr(visitor, "visit%s" % self.__class__.__name__)(self)


class Arguments(Argument):
    def __init__(self):
        self.arguments = []

    def append(self, argument):
        self.arguments.append(argument)

    def values(self):
        return self.arguments


class OptionalArgument(Argument):
    def __init__(self, name, message, **kwargs):
        names = name.split(',')
        if len(names) > 1:
            for n in names:
                if not n.startswith('-'):
                    raise ArgumentError(name)
        super(OptionalArgument, self).__init__(name, message, **kwargs)


class HelpArgument(OptionalArgument):
    pass


class PositionalArgument(Argument):
    pass


class GroupArgument(OptionalArgument):
    def __init__(self):
        self.arguments = []

    def add_argument(self, name, message=""):
        self.arguments = [x for x in self.arguments if x.name != name]
        argument = OptionalArgument(name, message)
        self.arguments.append(argument)


class Visitor(object):
    def visitArguments(self, args):
        pass

    def visitOptionalArgument(self, arg):
        pass

    def visitHelpArgument(self, arg):
        pass

    def visitPositionalArgument(self, arg):
        pass

    def visitGroupArgument(self, arg):
        pass


class UsageVisitor(Visitor):
    def visitArguments(self, args):
        prog = os.path.basename(sys.argv[0])
        return "Usage: %s %s" % (prog, " ".join([a.accept(self) for a in args.values()]))

    def visitOptionalArgument(self, arg):
        return "[" + arg.name + "]"

    def visitHelpArgument(self, arg):
        return "[" + arg.name + "]"

    def visitPositionalArgument(self, arg):
        return arg.name

    def visitGroupArgument(self, arg):
        return "[" + "|".join([a.name for a in arg.arguments]) + "]"


class LengthVisitor(Visitor):
    def visitArguments(self, args):
        return max([a.accept(self) for a in args.values()])

    def visitOptionalArgument(self, arg):
        return len(arg.name)

    def visitHelpArgument(self, arg):
        return len(arg.name)

    def visitPositionalArgument(self, arg):
        return len(arg.name)

    def visitGroupArgument(self, arg):
        return max([a.accept(self) for a in arg.arguments])


class ListVisitor(Visitor):
    def __init__(self):
        self.space = 4
        self.offset = 0

    def visitArguments(self, args):
        o = "\n".join([a.accept(self) for a in args.arguments if isinstance(a, OptionalArgument)])
        p = "\n".join([a.accept(self) for a in args.arguments if isinstance(a, PositionalArgument)])
        s = "Optional:\n%s\nPositional:\n%s"
        return s % (o, p)

    def visitOptionalArgument(self, arg):
        return arg.name.ljust(self.offset + self.space) + arg.message

    def visitHelpArgument(self, arg):
        return arg.name.ljust(self.offset + self.space) + arg.message

    def visitPositionalArgument(self, arg):
        return arg.name.ljust(self.offset + self.space) + arg.message

    def visitGroupArgument(self, arg):
        return "\n".join([argument.accept(self) for argument in arg.arguments])


class ParseVisitor(Visitor):
    def __init__(self):
        self.expression = None
        self.namespace = None

    def init(self, expression):
        self.expression = expression
        self.namespace = {}

    def visitArguments(self, args):
        for arg in args.values():
            arg.accept(self)
        if self.expression:
            raise IllegalArgException(" ".join(self.expression))

    def visitOptionalArgument(self, arg):
        for index, e in enumerate(self.expression):
            names = arg.name.split(',')
            if e in names:
                for n in names:
                    self.namespace[n.strip('-')] = True
                self.expression.pop(index)
                return

    def visitHelpArgument(self, arg):
        for e in self.expression:
            if e in arg.name.split(','):
                raise HelpException()

    def visitPositionalArgument(self, arg):
        for index, e in enumerate(self.expression):
            if not e.startswith('-'):
                self.namespace[arg.name] = e
                self.expression.pop(index)
                return
        raise NotEnoughArgException(" ".join(self.expression))

    def visitGroupArgument(self, arg):
        i = []
        for a in arg.arguments:
            for index, e in enumerate(self.expression):
                if e == a.name:
                    i.append((index, e))
        if len(i) > 1:
            raise InCompatibleArgException(" ".join([x[1] for x in i]))
        elif len(i) == 1:
            index, e = i[0]
            self.namespace[e.strip('-')] = True
            self.expression.pop(index)


class NameSpace(dict):
    def __getattr__(self, name):
        try:
            return self[name]
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
        self.arguments = Arguments()
        self.add_argument("-h,--help", message="show this help message and exit.")
        self.handler = handler()
        self.usage_visitor = UsageVisitor()
        self.length_visitor = LengthVisitor()
        self.list_visitor = ListVisitor()
        self.parse_visitor = ParseVisitor()

    def parse_arg(self, expression=(sys.argv)[1:]):
        try:
            namespace = NameSpace(self.parse(expression))
            return namespace
        except HelpException:
            self.print_help()
            sys.exit(0)
        except SargException, e:
            print(self.get_usage(), file=sys.stderr)
            print(e, file=sys.stderr)
            self.handler.handle(e)

    def add_argument(self, name, message="", **kwargs):
        if name == "-h,--help" or name in ["-h", "--help"]:
            argument = HelpArgument(name, message, **kwargs)
        elif name.startswith("-"):
            argument = OptionalArgument(name, message, **kwargs)
        else:
            argument = PositionalArgument(name, message, **kwargs)
        self.arguments.append(argument)

    def add_group_argument(self, group):
        self.arguments.append(group)

    def print_help(self):
        print(self.get_usage())
        self.list_visitor.offset = self.get_arguments_length()
        print
        print(self.get_arguments_list())

    def parse(self, expression):
        self.parse_visitor.init(expression)
        self.parse_visitor.visitArguments(self.arguments)
        return self.parse_visitor.namespace

    def get_arguments_length(self):
        return self.length_visitor.visitArguments(self.arguments)

    def get_usage(self):
        return self.usage_visitor.visitArguments(self.arguments)

    def get_arguments_list(self):
        return self.list_visitor.visitArguments(self.arguments)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
