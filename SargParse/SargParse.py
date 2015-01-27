import sys
import os


class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


class Action(Singleton):
    pass


class _HelpAction(Action):
    def __call__(self, name, expression, parser, namespace):
        for n in name.split(','):
            if n == expression:
                parser.print_help()
                parser.exit()


class _StoreAction(Action):
    def __call__(self, name, expression, parser, namespace):
        namespace[name] = expression
        return True


class _StoreTrueAction(Action):
    def __call__(self, name, expression, parser, namespace):
        for n in name.split(','):
            if n == expression:
                namespace[n] = True
                return True
        return False


class Argument(object):
    def __init__(self, name, action, type, message):
        self.name = name
        self.action = action
        self.type = type
        self.message = message

    def __call__(self, expression, parser, namespace):
        return self.action(self.name, expression, parser, namespace)


class GroupArgument(Argument):
    pass


ACTION_MAPPING = {'help': _HelpAction(),
                  'store': _StoreAction(),
                  'storeTrue': _StoreTrueAction()}


class SargParser(object):
    def __init__(self):
        ## init
        self.prog = os.path.basename(sys.argv[0])
        self.arguments = []
        self.add_argument("-h,--help", mode="optional", action="help", message="show this help message and exit.")

    def parse_arg(self, expression=sys.argv[1:]):
        try:
            namespace = self.parse(expression)
            return namespace
        except Exception, e:
            self.error(e.message)

    def add_argument(self, name, mode="positional", action="store", message=""):
        action = ACTION_MAPPING[action]
        self.arguments.append(Argument(name, action, mode, message))

    def print_help(self):
        self.print_usage()
        l = self.max_argument_length()
        space = 4
        print
        print "Optional:"
        for oa in self.get_arguments_by_type("optional"):
            print oa.name.ljust(l + space) + oa.message
        print
        print "Positional:"
        for pa in self.get_arguments_by_type("positional"):
            print pa.name.ljust(l + space) + pa.message

    def parse(self, expression):
        def parse_rest(positional_arguments, optional_arguments, expression, namespace):
            if len(expression) == 0 and len(positional_arguments) == 0:
                return namespace
            elif len(expression) == 0 and len(positional_arguments) > 0:
                raise Exception("Not enough arguments.")
            else:
                for optional_argument in optional_arguments:
                        if optional_argument(expression[0], self, namespace):
                            return parse_rest(positional_arguments, [a for a in optional_arguments if a != optional_argument], expression[1:], namespace)
                if len(positional_arguments) == 0:
                    raise Exception("Too many arguments.")
                elif positional_arguments[0](expression[0], self, namespace):
                    return parse_rest(positional_arguments[1:], optional_arguments, expression[1:], namespace)
                else:
                    raise Exception("Illegal argument " + expression[0])
        namespace = parse_rest(self.get_arguments_by_type("positional"), self.get_arguments_by_type("optional"), expression, {})
        return namespace

    def get_arguments_by_type(self, type):
        return [argument for argument in self.arguments if argument.type == type]

    def max_argument_length(self):
        return max(map(lambda x: len(x.name),self.arguments))

    def get_arguments(self):
        return " ".join(["[" + x.name + "]" for x in self.get_arguments_by_type("optional")]) + " " + " ".join(["[" + x.name + "]" for x in self.get_arguments_by_type("positional")])

    def exit(self):
        sys.exit(0)

    def error(self, error_message):
        self.print_usage()
        print error_message
        sys.exit(0)

    def print_usage(self):
        print "Usage: " + self.prog + " " + self.get_arguments()

