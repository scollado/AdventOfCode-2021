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
        expected_first_point = MapPoint(parent_map=sut,
                                        x=0, y=0,
                                        depth=2)
        expected_second_row_first_point = MapPoint(parent_map=sut,
                                                   x=0, y=1,
                                                   depth=3)
        expected_last_point = MapPoint(parent_map=sut,
                                       x=sut.width - 1, y=sut.height - 1,
                                       depth=8)

        self.assertEqual(expected_first_point, sut[(0, 0)])
        self.assertEqual(expected_second_row_first_point, sut[(0, 1)])
        self.assertEqual(expected_last_point, sut[(sut.width - 1, sut.height - 1)])


class TestMapPoint(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.heightmap = HeightMap(EXAMPLE_INPUT.split("\n"))

    def test_top_neighbor(self):
        first_point_on_second_row: MapPoint = self.heightmap.points[10]

        first_point_on_first_row: MapPoint = self.heightmap.points[0]

        self.assertEqual(first_point_on_first_row, first_point_on_second_row.top_neighbor())

    def test_top_neighbor_is_None(self):
        first_point_on_first_row: MapPoint = self.heightmap.points[0]

        self.assertIsNone(first_point_on_first_row.top_neighbor())

    def test_right_neighbor(self):
        first_point: MapPoint = self.heightmap.points[0]

        expected_neighbor: MapPoint = self.heightmap.points[1]

        self.assertEqual(expected_neighbor, first_point.right_neighbor())

    def test_right_neighbor_is_None(self):
        last_point = self.heightmap.points[-1]

        self.assertIsNone(last_point.right_neighbor())

    def test_down_neighbor(self):
        first_point_on_first_row: MapPoint = self.heightmap.points[0]

        first_point_on_second_row: MapPoint = self.heightmap.points[10]

        self.assertEqual(first_point_on_second_row, first_point_on_first_row.down_neighbor())

    def test_down_neighbor_is_None(self):
        last_point = self.heightmap.points[-1]

        self.assertIsNone(last_point.down_neighbor())

    def test_left_neighbor(self):
        second_point_on_first_row: MapPoint = self.heightmap.points[1]

        first_point_on_first_row: MapPoint = self.heightmap.points[0]

        self.assertEqual(first_point_on_first_row, second_point_on_first_row.left_neighbor())

    def test_left_neighbor_is_None(self):
        first_point = self.heightmap.points[0]
        self.assertIsNone(first_point.left_neighbor())
