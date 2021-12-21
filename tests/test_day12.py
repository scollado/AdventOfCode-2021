from unittest import TestCase

from day12 import Day12

SIMPLE_EXAMPLE_INPUT = '''
start-A
start-b
A-c
A-b
b-d
A-end
b-end
'''.strip()

SIMPLE_EXAMPLE_EXPECTED_COUNT = 10
SIMPLE_EXAMPLE_PART_2_EXPECTED_COUNT = 36

COMPLEX_EXAMPLE_INPUT = '''
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
'''.strip()

COMPLEX_EXAMPLE_PATH_COUNT = 226

EXPECTED_PATH_LIST = sorted([
    'start,A,b,A,c,A,end',
    'start,A,b,A,end',
    'start,A,b,end',
    'start,A,c,A,b,A,end',
    'start,A,c,A,b,end',
    'start,A,c,A,end',
    'start,A,end',
    'start,b,A,c,A,end',
    'start,b,A,end',
    'start,b,end'
])


class TestDay12(TestCase):

    def setUp(self) -> None:
        self.sut = Day12(SIMPLE_EXAMPLE_INPUT.split("\n"))

    def test_complex_example(self):
        complex_sut = Day12(COMPLEX_EXAMPLE_INPUT.split("\n"))
        self.assertEqual(COMPLEX_EXAMPLE_PATH_COUNT, complex_sut.part_one())

    def test_part_one(self):
        self.assertEqual(SIMPLE_EXAMPLE_EXPECTED_COUNT, self.sut.part_one())

    def test_part_two(self):
        self.assertEqual(SIMPLE_EXAMPLE_PART_2_EXPECTED_COUNT, self.sut.part_two())
