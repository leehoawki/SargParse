import unittest
from subprocess import check_output

class TestPythonPy(unittest.TestCase):
    def test_numbers(self):
        self.assertEqual(check_output(['py', '3 * 4.5']),'13.5\n')

    def test_range(self):
        self.assertEqual(check_output(['py', 'range(3)']), '\n'.join(map(str, range(3))) + '\n')

    def test_split_input(self):
        self.assertEqual(check_output(["""echo a,b | py -x 'x.split(",")[1]' """], shell=True), 'b\n')

    def test_filter(self):
        self.assertEqual(check_output("""py 'range(0,4)' | py -f 'int(x)==3'""", shell=True), '3\n')

    def test_reduce(self):
        self.assertEqual(check_output("""py 'range(0,4)' | py -r 'int(x)+int(y)'""", shell=True), '6\n')

    def test_listp(self):
        self.assertEqual(check_output("""py 'range(0,3)' | py -l 'x[::-1]'""", shell=True), '\n'.join(map(str, range(3)[::-1])) + '\n')
        self.assertEqual(check_output("""py 'range(0,3)' | py -l 'x[1]'""", shell=True), '1\n')

    def test_imports(self):
        module_commands = ["math.ceil(2.5)",
                           "base64.b64encode('data to be encoded')",
                           "calendar.weekday(1955, 11, 5)",
                           "csv.list_dialects()",
                           "datetime.timedelta(hours=-5)",
                           "hashlib.sha224(\"Nobody inspects the spammish repetition\").hexdigest()",
                           "glob.glob('*')",
                           "itertools.product(['a','b'], [1,2])",
                           "json.dumps([1,2,3,{'4': 5, '6': 7}], separators=(',',':'))",
                           "os.name",
                           "random.randint(0, 1000)",
                           "re.compile('[a-z]').findall('abcd')",
                           "shutil.get_archive_formats()",
                           "tempfile.gettempdir()",
                           "uuid.uuid1()",
                           ]
        for command in module_commands:
            check_output("py %r" % command, shell=True)

if __name__ == '__main__':
    unittest.main()
