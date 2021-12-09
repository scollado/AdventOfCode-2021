from unittest import TestCase

from day06 import LanterFishGeneration

EXAMPLE_INPUT = '3,4,3,1,2'
EXPECTED_DAY_18_COUNT = 26
EXPECTED_DAY_80_COUNT = 5934
EXPECTED_DAY_256_COUNT = 26984457539


class TestLanterFishGeneration(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self._generation = LanterFishGeneration(EXAMPLE_INPUT)

    def test_pass_18_days(self):
        self._generation.pass_days(18)

        self.assertEqual(EXPECTED_DAY_18_COUNT, len(self._generation))

    def test_pass_80_days(self):
        self._generation.pass_days(80)

        self.assertEqual(EXPECTED_DAY_80_COUNT, len(self._generation))

    def test_pass_256_days(self):
        self._generation.pass_days(256)

        self.assertEqual(EXPECTED_DAY_256_COUNT, len(self._generation))
