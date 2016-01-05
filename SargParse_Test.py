import unittest
import SargParse


class SargParse_Test(unittest.TestCase):
    def test_basic_arguments(self):
        s = SargParse.SargParser()
        s.add_argument('-x', message='x factor')
        s.add_argument('-y', message='y factor')
        s.add_argument('exp', message='expression')
        namespace = s.parse_arg(['exp'])







    def test_group_arguments(self):
        s = SargParse.SargParser()
        group = SargParse.GroupArgument()
        group.add_argument('-a', message='a factor')
        group.add_argument('-b', message='b factor')
        group.add_argument('-c', message='c factor')
        s.add_group_argument(group)
        s.add_argument('exp', message='expression')
        namespace = s.parse_arg()


if __name__ == '__main__':
    unittest.main()
