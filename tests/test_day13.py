from unittest import TestCase

from day13 import Day13, TransparentSheet

EXAMPLE_INPUT = '''
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
'''.strip()

EXPECTED_FOLDING_PART_ONE = [
    '11111',
    '10001',
    '10001',
    '10001',
    '11111',
    '00000',
    '00000'
]

EXPECTED_POINT_COUNT_PART_ONE = 17


class TestDay13(TestCase):
    sut: Day13

    @classmethod
    def setUpClass(cls) -> None:
        cls.sut = Day13(EXAMPLE_INPUT.split("\n"))

    def test_part_one(self):
        self.assertEqual(EXPECTED_POINT_COUNT_PART_ONE, self.sut.part_one())

    def test_part_two(self):
        expected_sheet = TransparentSheet(EXPECTED_FOLDING_PART_ONE)

        self.assertEqual(expected_sheet, self.sut.apply_folding(self.sut.folds))


class TestTransparentSheet(TestCase):
    def test_matrix_addition(self):
        first_data = [
            '111',
            '000',
            '101'
        ]
        first = TransparentSheet(first_data)

        second_data = [
            '000',
            '111',
            '010'
        ]
        second = TransparentSheet(second_data)

        expected_data = [
            '111',
            '111',
            '111'
        ]
        expected = TransparentSheet(expected_data)

        self.assertEqual(expected, first + second)

    def test_fold_vertical(self):
        start_matrix = [
            '10101',
            '01010',
            '11011'
        ]
        sut = TransparentSheet(start_matrix)

        expected_matrix = [
            '10',
            '01',
            '11'
        ]
        expected_folded = TransparentSheet(expected_matrix)

        self.assertEqual(expected_folded, sut.vfold(2))

    def test_fold_horizontal(self):
        start_matrix = [
            '101',
            '010',
            '110'
        ]
        sut = TransparentSheet(start_matrix)

        expected_matrix = [
            '111'
        ]
        expected_folded = TransparentSheet(expected_matrix)

        self.assertEqual(expected_folded, sut.hfold(1))
