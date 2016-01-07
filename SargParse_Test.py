import unittest
import SargParse


class SargParse_Test(unittest.TestCase):
    s = None
    a = None

    def setUp(self):
        global s
        s = SargParse.SargParser(handler=SargParse.DebugErrorHandler)
        s.add_argument('-x', message='x factor')
        s.add_argument('-y', message='y factor')
        s.add_argument('exp', message='expression')

        global a
        a = SargParse.SargParser(handler=SargParse.DebugErrorHandler)
        group = SargParse.GroupArgument()
        group.add_argument('-a', message='a factor')
        group.add_argument('-b', message='b factor')
        group.add_argument('-c', message='c factor')
        a.add_group_argument(group)
        a.add_argument('exp', message='expression')

    def test_basic_arguments(self):
        global s
        namespace = s.parse_arg(['exp'])
        assert namespace.exp == 'exp'
        assert not namespace.x
        assert not namespace.y

        namespace = s.parse_arg(['-x', 'exp'])
        assert namespace.exp == 'exp'
        assert namespace.x
        assert not namespace.y

        namespace = s.parse_arg(['-x', '-y', 'exp'])
        assert namespace.exp == 'exp'
        assert namespace.x
        assert namespace.y

    def test_group_arguments(self):
        global a

        namespace = a.parse_arg(['exp'])
        assert namespace.exp == 'exp'
        assert not namespace.a
        assert not namespace.b
        assert not namespace.c

        namespace = a.parse_arg(['-a', 'exp'])
        assert namespace.exp == 'exp'
        assert namespace.a
        assert not namespace.b
        assert not namespace.c

    def test_too_many_exception(self):
        e = False
        try:
            namespace = s.parse_arg(['-x', '-y', 'exp', 'fuck'])
        except SargParse.IllegalArgException, e:
            e = True
        assert e

    def test_not_enough_exception(self):
        e = False
        try:
            namespace = s.parse_arg([])
        except SargParse.NotEnoughArgException, e:
            e = True
        assert e

    def test_illegal_exception(self):
        e = False
        try:
            namespace = s.parse_arg(['-a', 'exp'])
        except SargParse.IllegalArgException, e:
            e = True
        assert e

    def test_conflict_exception(self):
        e = False
        try:
            namespace = a.parse_arg(['-a', '-b', 'exp'])
        except SargParse.InCompatibleArgException, e:
            e = True
        assert e


if __name__ == '__main__':
    unittest.main()
