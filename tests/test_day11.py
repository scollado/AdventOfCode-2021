from unittest import TestCase

from day11 import OctopusesMap, Day11

EXAMPLE_INPUT = '''
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
'''.strip()

EXAMPLE_TICK_1 = '''
6594254334
3856965822
6375667284
7252447257
7468496589
5278635756
3287952832
7993992245
5957959665
6394862637
'''.strip()

EXAMPLE_TICK_2 = '''
8807476555
5089087054
8597889608
8485769600
8700908800
6600088989
6800005943
0000007456
9000000876
8700006848
'''.strip()

EXPECTED_100_TICKS_FLASH_COUNT = 1656

EXPECTED_TICK_COUNT_PART_TWO = 195

SMALL_EXAMPLE_STARTING_POINT = '''
11111
19991
19191
19991
11111
'''.strip()

SMALL_EXAMPLE_TICK_1 = '''
34543
40004
50005
40004
34543
'''.strip()

SMALL_EXAMPLE_TICK_2 = '''
45654
51115
61116
51115
45654
'''.strip()


class TestDay11(TestCase):
    def test_part_one(self):
        sut = Day11(EXAMPLE_INPUT.split("\n"))

        self.assertEqual(EXPECTED_100_TICKS_FLASH_COUNT, sut.part_one())

    def test_part_two(self):
        sut = Day11(EXAMPLE_INPUT.split("\n"))

        self.assertEqual(EXPECTED_TICK_COUNT_PART_TWO, sut.part_two())


class TestOctopusMap(TestCase):

    def test_tick_example_sequence(self):
        test_map = OctopusesMap(SMALL_EXAMPLE_STARTING_POINT.split("\n"))
        test_map.tick()
        self.assertEqual(SMALL_EXAMPLE_TICK_1, str(test_map))
        test_map.tick()
        self.assertEqual(SMALL_EXAMPLE_TICK_2, str(test_map))


class TestFlashingOctupus(TestCase):

    def setUp(self) -> None:
        self.test_map = OctopusesMap(['111', '191', '111'])

    def test_flashing_octopus(self):
        center_octopus = self.test_map[(1, 1)]
        center_octopus.value += 1
        self.assertTrue(center_octopus.flash())

    def test_flashing_octopus_energy_propagation(self):
        center_octopus = self.test_map[(1, 1)]
        center_octopus.value += 1
        expected_neighbor_values = {(neighbor.x, neighbor.y): neighbor.value + 1
                                    for neighbor in center_octopus.neighbors()}
        center_octopus.flash()

        result = {(neighbor.x, neighbor.y): neighbor.value
                  for neighbor in center_octopus.neighbors()}

        self.assertDictEqual(expected_neighbor_values, result)
