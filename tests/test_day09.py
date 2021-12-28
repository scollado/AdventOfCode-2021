from unittest import TestCase

from day09 import Day09, HeightMap, MapPoint

EXAMPLE_INPUT = '''
2199943210
3987894921
9856789892
8767896789
9899965678
'''.strip()

EXPECTED_RISK_LEVEL_PART_ONE = 15

EXPECTED_PART_TWO_RESULT = 1134


class TestDay09(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.sut = Day09(EXAMPLE_INPUT.split("\n"))

    def test_part_one(self):
        self.assertEqual(EXPECTED_RISK_LEVEL_PART_ONE, self.sut.part_one())

    def test_part_two(self):
        self.assertEqual(EXPECTED_PART_TWO_RESULT, self.sut.part_two())


class TestHeightMap(TestCase):
    def test_getitem(self):
        sut = HeightMap(EXAMPLE_INPUT.split("\n"))
        expected_first_point = MapPoint(sut,
                                        x=0, y=0,
                                        value=2)
        expected_second_row_first_point = MapPoint(sut,
                                                   x=0, y=1,
                                                   value=3)
        expected_last_point = MapPoint(sut,
                                       x=sut.max_x - 1, y=sut.max_y - 1,
                                       value=8)

        self.assertEqual(expected_first_point, sut[(0, 0)])
        self.assertEqual(expected_second_row_first_point, sut[(0, 1)])
        self.assertEqual(expected_last_point, sut[(sut.max_x - 1, sut.max_y - 1)])


class TestMapPoint(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.heightmap = HeightMap(EXAMPLE_INPUT.split("\n"))

    def test_top_neighbor(self):
        first_point_on_second_row: MapPoint = self.heightmap.cells[10]

        first_point_on_first_row: MapPoint = self.heightmap.cells[0]

        self.assertEqual(first_point_on_first_row, first_point_on_second_row.top())

    def test_top_neighbor_is_None(self):
        first_point_on_first_row: MapPoint = self.heightmap.cells[0]

        self.assertIsNone(first_point_on_first_row.top())

    def test_right_neighbor(self):
        first_point: MapPoint = self.heightmap.cells[0]

        expected_neighbor: MapPoint = self.heightmap.cells[1]

        self.assertEqual(expected_neighbor, first_point.right())

    def test_right_neighbor_is_None(self):
        last_point = self.heightmap.cells[-1]

        self.assertIsNone(last_point.right())

    def test_down_neighbor(self):
        first_point_on_first_row: MapPoint = self.heightmap.cells[0]

        first_point_on_second_row: MapPoint = self.heightmap.cells[10]

        self.assertEqual(first_point_on_second_row, first_point_on_first_row.bottom())

    def test_down_neighbor_is_None(self):
        last_point = self.heightmap.cells[-1]

        self.assertIsNone(last_point.bottom())

    def test_left_neighbor(self):
        second_point_on_first_row: MapPoint = self.heightmap.cells[1]

        first_point_on_first_row: MapPoint = self.heightmap.cells[0]

        self.assertEqual(first_point_on_first_row, second_point_on_first_row.left())

    def test_left_neighbor_is_None(self):
        first_point = self.heightmap.cells[0]
        self.assertIsNone(first_point.left())
