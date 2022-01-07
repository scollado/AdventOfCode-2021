from unittest import TestCase

from day17 import read_target_area, LaunchAttempt, Day17

PART_ONE_EXAMPLE_INPUT = 'target area: x=20..30, y=-10..-5'


class TestDay17(TestCase):
    def test_example_probe_launch(self):
        target = read_target_area(PART_ONE_EXAMPLE_INPUT)
        launch = LaunchAttempt((6, 9), target)

        self.assertTrue(launch.probe in target)
        self.assertEqual(45, launch.max_height())

    def test_part_two(self):
        expected_successes = 112
        sut = Day17([PART_ONE_EXAMPLE_INPUT])

        self.assertEqual(expected_successes, sut.part_two())
