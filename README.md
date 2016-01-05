SargParser
====

This is just another argparser like the one python standard library offers.

Basic Examples:

    import SargParse
    s = SargParse.SargParser()
    s.add_argument('-x', message='x factor')
    s.add_argument('-y', message='y factor')
    s.add_argument('exp', message='expression')
    namespace = s.parse_arg()
    
    ./test1 --help
    Usage: test1.py [-h,--help] [-x] [-y] exp

    Optional:
    -h,--help    show this help message and exit.
    -x           x factor
    -y           y factor
    
    Positional:
    exp          expression

There are also some advanced features like group arguments.

    import SargParse
    s = SargParse.SargParser()
    group = SargParse.GroupArgument()
    group.add_argument('-a', message='a factor')
    group.add_argument('-b', message='b factor')
    group.add_argument('-c', message='c factor')
    s.add_group_argument(group)
    s.add_argument('exp', message='expression')
    namespace = s.parse_arg()
    
    ./test2 --help
    Usage: test2.py [-h,--help] [-a|-b|-c] exp

    Optional:
    -h,--help    show this help message and exit.
    -a           a factor
    -b           b factor
    -c           c factor
    
    Positional:
    exp          expression
    
    
    
    
