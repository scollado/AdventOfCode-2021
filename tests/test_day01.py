from unittest import TestCase

from day01 import Day01, get_increment_value, SmoothedSonarReport


class TestDay1(TestCase):
    EXPECTED_RESULT_P1 = 7
    EXPECTED_RESULT_P2 = 5
    SONAR_REPORT = [
        199,
        200,
        208,
        210,
        200,
        207,
        240,
        269,
        260,
        263
    ]
    SMOOTHED_REPORT = [
        607,
        618,
        618,
        617,
        647,
        716,
        769,
        792,
    ]

    def test_get_increment_value_should_return_zero_when_previous_is_None(self):
        self.assertEqual(0, get_increment_value(current=1, previous=None))

    def test_get_increment_value_should_return_zero_when_current_is_lower_than_previous(self):
        self.assertEqual(0, get_increment_value(current=1, previous=2))

    def test_get_increment_value_should_return_one_when_current_is_greater_than_previous(self):
        self.assertEqual(1, get_increment_value(current=3, previous=2))

    def test_get_increment_value_should_return_zero_when_current_is_equal_to_previous(self):
        self.assertEqual(0, get_increment_value(current=0, previous=0))

    def test_smoothedsonarreport_result(self):
        self.assertListEqual(list(SmoothedSonarReport(TestDay1.SONAR_REPORT).sweep_values), TestDay1.SMOOTHED_REPORT)

    def test_part_one(self):
        sut = Day01(TestDay1.SONAR_REPORT)
        self.assertEqual(TestDay1.EXPECTED_RESULT_P1, sut.part_one())

    def test_part_two(self):
        sut = Day01(TestDay1.SONAR_REPORT)
        self.assertEqual(TestDay1.EXPECTED_RESULT_P2, sut.part_two())
