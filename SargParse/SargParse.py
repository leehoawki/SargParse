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
        if expression == '-h' or expression == '--help':
            parser.printHelp()
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

class Argument():
    def __init__(self, name, action, type, message):
        self.name = name
        self.action = action
        self.type = type
        self.message = message

    def __call__(self, expression, parser, namespace):
        return self.action(self.name, expression, parser, namespace)

class Arguments():
    def __init__(self, parser):
        self.parser = parser
        self.arguments = []

    def addArgument(self, argument):
        self.arguments.append(argument)

    def getOptionalArguments(self):
        return [argument for argument in self.arguments if argument.type == "optional"]

    def getPositionalArguments(self):
        return [argument for argument in self.arguments if argument.type == "positional"]

    def maxArgumentLength(self):
        return max(map(lambda x:len(x.name),self.arguments))

    def __str__(self):
        return " ".join(map(lambda x : "[" + x.name + "]", self.getOptionalArguments())) + " " + " ".join(map(lambda x : x.name, self.getPositionalArguments()))

    def parse(self, expression):
        def parseRest(positionalArguments, optionalArguments, expression, namespace):
            if len(expression) == 0 and len(positionalArguments) == 0:
                return namespace
            elif len(expression) == 0 and len(positionalArguments) > 0:
                raise Exception("Not enough arguments.")
            elif len(positionalArguments) == 0 and len(expression) > 0:
                raise Exception("Too many arguments.")
            else:
                for optionalArgument in optionalArguments:
                        if optionalArgument(expression[0], self.parser, namespace):
                            return parseRest(positionalArguments, [a for a in optionalArguments if a != optionalArgument], expression[1:], namespace)
                if positionalArguments[0](expression[0], self.parser, namespace):
                    return parseRest(positionalArguments[1:], optionalArguments, expression[1:], namespace)
                else:
                    raise Exception("Illegal argument " + expression[0])
        namespace = parseRest(self.getPositionalArguments(),self.getOptionalArguments(), expression, {})
        return namespace

actionMapping = {}
actionMapping['help'] = _HelpAction()
actionMapping['store'] = _StoreAction()
actionMapping['storeTrue'] = _StoreTrueAction()

class SargParser():
    def __init__(self):
        ## init
        self.prog = os.path.basename(sys.argv[0])
        self.arguments = Arguments(self)
        self.addArgument("-h,--help", type="optional", action="help", message="show this help message and exit.")

    def parseArg(self, expression=sys.argv[1:]):
        return self.arguments.parse(expression)
        # try:
        #     namespace = self.arguments.parse(expression)
        #     return namespace
        # except Exception, e:
        #     self.error(e.message)

    def addArgument(self, name, type = "positional", action = "store", message = ""):
        action = actionMapping[action]
        self.arguments.addArgument(Argument(name, action, type, message))

    def printHelp(self):
        self.printUsage()
        l = self.arguments.maxArgumentLength()
        space = 4
        print "Optional:"
        for oa in self.arguments.getOptionalArguments():
            print oa.name.ljust(l + space) + oa.message
        print
        print "Positional:"
        for pa in self.arguments.getPositionalArguments():
            print pa.name.ljust(l + space) + pa.message

    def exit(self):
        sys.exit(0)

    def error(self, errorMessage):
        self.printUsage()
        print errorMessage
        sys.exit(0)

    def printUsage(self):
        print "Usage: " + self.prog + " " + str(self.arguments)


if __name__ == '__main__':
    parser = SargParser()
    parser.addArgument('-x', action="storeTrue", type = "optional" , message = "x factor")
    parser.addArgument('exp', action="store", message='lambda expression.')
    namespace = parser.parseArg()
