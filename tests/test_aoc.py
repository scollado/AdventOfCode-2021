from unittest import TestCase

from aocutils.matrix import Matrix

INPUT_MATRIX = '''
00011
00011
00000
22000
22000
'''.strip()


class TestMatrix(TestCase):

    def setUp(self) -> None:
        self.input_matrix = Matrix(INPUT_MATRIX.split("\n"))

    def test_vsplit(self):
        expected_left_matrix = Matrix([
            '00',
            '00',
            '00',
            '22',
            '22'
        ])
        expected_right_matrix = Matrix([
            '11',
            '11',
            '00',
            '00',
            '00'
        ])
        left_result, right_result = self.input_matrix.vsplit(2)
        self.assertEqual(expected_left_matrix, left_result)
        self.assertEqual(expected_right_matrix, right_result)

    def test_hsplit(self):
        expected_top_matrix = Matrix([
            '00011',
            '00011'
        ])
        expected_bottom_matrix = Matrix([
            '22000',
            '22000'
        ])

        top_result, bottom_result = self.input_matrix.hsplit(2)
        self.assertEqual(expected_top_matrix, top_result)
        self.assertEqual(expected_bottom_matrix, bottom_result)

    def test_vflip(self):
        expected_flipped = Matrix('''
        22000
        22000
        00000
        00011
        00011
        '''.strip().split("\n"))

        self.assertEqual(expected_flipped, self.input_matrix.vflip())

    def test_hflip(self):
        expected_flipped = Matrix('''
        11000
        11000
        00000
        00022
        00022
        '''.strip().split("\n"))

        self.assertEqual(expected_flipped, self.input_matrix.hflip())
