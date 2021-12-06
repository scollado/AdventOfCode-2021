from unittest import TestCase

from day03 import DiagnosticReport, filter_by_most_common_value_at_rank, filter_by_least_common_value_at_rank


class TestDay3(TestCase):
    DIAGNOSTIC_REPORT = [
        '00100',
        '11110',
        '10110',
        '10111',
        '10101',
        '01111',
        '00111',
        '11100',
        '10000',
        '11001',
        '00010',
        '01010']
    EXPEXTED_GAMMA = 22  # 0b10110
    EXPECTED_EPSILON = 9  # 0b01001
    EXPECTED_CONSUMPTION = 198  # 22 * 9
    EXPECTED_O2_RATING = 23  # 0b10111
    EXPECTED_CO2_RATING = 10  # 0b01010
    EXPECTED_LIFE_SUPPORT_RATING = 230  # 23 * 10

    EXPECTED_RANK0_O2_LIST = [
        '11110',
        '10110',
        '10111',
        '10101',
        '11100',
        '10000',
        '11001',
    ]
    EXPECTED_RANK0_CO2_LIST = [
        '00100',
        '01111',
        '00111',
        '00010',
        '01010'
    ]

    def test_gamma_rate_provides_expected_value(self):
        sut = DiagnosticReport(TestDay3.DIAGNOSTIC_REPORT)

        self.assertEqual(TestDay3.EXPEXTED_GAMMA, sut.gamma_rate)

    def test_epsilon_rate_provides_expected_value(self):
        sut = DiagnosticReport(TestDay3.DIAGNOSTIC_REPORT)

        self.assertEqual(TestDay3.EXPECTED_EPSILON, sut.epsilon_rate)

    def test_consumption_provides_expected_value(self):
        sut = DiagnosticReport(TestDay3.DIAGNOSTIC_REPORT)

        self.assertEqual(TestDay3.EXPECTED_CONSUMPTION, sut.consumption())

    def test_filter_by_most_common_value_at_rank_returns_expected_values(self):
        filtered_list: list[str] = filter_by_most_common_value_at_rank(TestDay3.DIAGNOSTIC_REPORT, 0)

        self.assertListEqual(TestDay3.EXPECTED_RANK0_O2_LIST, filtered_list)

    def test_filter_by_least_common_value_at_rank_returns_expected_values(self):
        filtered_list: list[str] = filter_by_least_common_value_at_rank(TestDay3.DIAGNOSTIC_REPORT, 0)

        self.assertListEqual(TestDay3.EXPECTED_RANK0_CO2_LIST, filtered_list)

    def test_rate_oxygen_generator(self):
        sut = DiagnosticReport(TestDay3.DIAGNOSTIC_REPORT)

        self.assertEqual(TestDay3.EXPECTED_O2_RATING, sut.rate_oxygen_generator())

    def test_rate_carbon_dioxyde_scrubber(self):
        sut = DiagnosticReport(TestDay3.DIAGNOSTIC_REPORT)

        self.assertEqual(TestDay3.EXPECTED_CO2_RATING, sut.rate_carbon_dioxyde_scrubber())

    def test_rate_life_support(self):
        sut = DiagnosticReport(TestDay3.DIAGNOSTIC_REPORT)

        self.assertEqual(TestDay3.EXPECTED_LIFE_SUPPORT_RATING, sut.rate_life_support())
