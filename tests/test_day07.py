from unittest import TestCase

from day07 import ConstantCostCrabFormation, LinearCostCrabFormation

EXAMPLE_POSITIONS = "16,1,2,0,4,2,7,1,2,14"
EXPECTED_CONSTANT_FUEL_CONSUMPTION = 37
EXPECTED_CONSTANT_TARGET_POSITION = 2
EXPECTED_LINEAR_TARGET_POSITION = 5
EXPECTED_LINEAR_FUEL_CONSUMPTION = 168


class TestConstantCostCrabFormation(TestCase):

    def setUp(self) -> None:
        self.crabs = ConstantCostCrabFormation([int(pos) for pos in EXAMPLE_POSITIONS.split(',')])

    def test_target_position(self):
        self.assertEqual(EXPECTED_CONSTANT_TARGET_POSITION, self.crabs.target_position)

    def test_fuel_consumption(self):
        self.assertEqual(EXPECTED_CONSTANT_FUEL_CONSUMPTION, self.crabs.fuel_consumption())


class TestLinearCostCrabFormation(TestCase):

    def setUp(self) -> None:
        self.crabs = LinearCostCrabFormation([int(pos) for pos in EXAMPLE_POSITIONS.split(',')])

    def test_target_position(self):
        self.assertEqual(EXPECTED_LINEAR_TARGET_POSITION, self.crabs.target_position)

    def test_fuel_consumption(self):
        self.assertEqual(EXPECTED_LINEAR_FUEL_CONSUMPTION, self.crabs.fuel_consumption())
