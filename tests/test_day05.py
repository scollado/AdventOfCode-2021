from unittest import TestCase

from day05 import Segment, VentMap, Day05

EXAMPLE_INPUT = """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""".strip()

EXPECTED_ORTHOGONAL_MAP = """
.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....
""".strip()

EXPECTED_COMPLETE_MAP = """
1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....
""".strip()

EXPECTED_ORTHOGONAL_RESULT = 5
EXPECTED_COMPLETE_RESULT = 12

EXAMPLE_SEGMENT = "1,2 -> 10,11"
EXAMPLE_VERTICAL = "1,2 -> 1,4"
EXAMPLE_HORIZONTAL = "1,2 -> 4,2"


class TestSegment(TestCase):
    def test_from_string(self):
        sut = Segment.from_string(EXAMPLE_SEGMENT)
        self.assertEqual(1, sut.start.x)
        self.assertEqual(2, sut.start.y)
        self.assertEqual(10, sut.end.x)
        self.assertEqual(11, sut.end.y)

    def test_is_vertical(self):
        sut = Segment.from_string(EXAMPLE_VERTICAL)

        self.assertTrue(sut.is_vertical())

    def test_is_horizontal(self):
        sut = Segment.from_string(EXAMPLE_HORIZONTAL)

        self.assertTrue(sut.is_horizontal())

    def test_is_oblique(self):
        sut = Segment.from_string(EXAMPLE_SEGMENT)

        self.assertTrue(sut.is_oblique())

    def test_horizontal_iterating(self):
        sut = Segment.from_string(EXAMPLE_HORIZONTAL)
        self.assertEqual(4, len(list(sut)))

    def test_vertical_iterating(self):
        sut = Segment.from_string(EXAMPLE_VERTICAL)
        self.assertEqual(3, len(list(sut)))


class TestVentMap(TestCase):
    def test_draw_orthonogal(self):
        sut = VentMap([segment
                       for segment in [Segment.from_string(line.strip()) for line in EXAMPLE_INPUT.split("\n")]
                       if not segment.is_oblique()])

        self.assertEqual(EXPECTED_ORTHOGONAL_MAP, sut.draw())

    def test_draw_complete(self):
        sut = VentMap([Segment.from_string(line.strip()) for line in EXAMPLE_INPUT.split("\n")])

        self.assertEqual(EXPECTED_COMPLETE_MAP, sut.draw())


class TestDay05(TestCase):
    def test_part_one(self):
        sut = Day05(EXAMPLE_INPUT.split("\n"))
        self.assertEqual(EXPECTED_ORTHOGONAL_RESULT, sut.part_one())

    def test_part_two(self):
        sut = Day05(EXAMPLE_INPUT.split("\n"))
        self.assertEqual(EXPECTED_COMPLETE_RESULT, sut.part_two())
