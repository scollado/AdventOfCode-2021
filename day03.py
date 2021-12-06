from collections import Counter
from typing import Tuple

from aocutils.aoc import Exercise
from aocutils.file import get_input_data_filepath


def filter_by_most_common_value_at_rank(input_values: list[str], position: int) -> list[str]:
    flipped_values = list(zip(*input_values))
    most_common, least_common = Counter(flipped_values[position]).most_common()
    filter_value = most_common[0]
    if most_common[1] == least_common[1]:
        filter_value = '1'

    return [line for line in input_values if line[position] == filter_value]


def filter_by_least_common_value_at_rank(input_values: list[str], position: int) -> list[str]:
    flipped_values = list(zip(*input_values))
    most_common, least_common = Counter(flipped_values[position]).most_common()
    filter_value = least_common[0]

    if most_common[1] == least_common[1]:
        filter_value = '0'

    return [line for line in input_values if line[position] == filter_value]


class DiagnosticReport:

    def __init__(self, report_lines: list[str]) -> None:
        super().__init__()

        self.report_lines = [line.strip() for line in report_lines]
        self.flipped_values = list(zip(*self.report_lines))

        epsilon, gamma = self._distribute_gamma_epsilon()

        self.gamma_rate = int(gamma, 2)
        self.epsilon_rate = int(epsilon, 2)

        self.oxygen_rating = 0
        self.co2_rating = 0

    def _distribute_gamma_epsilon(self) -> Tuple[str, str]:
        gamma = ""
        epsilon = ""
        for column in self.flipped_values:
            occurences = Counter(column).most_common()
            gamma += occurences[0][0]
            epsilon += occurences[-1][0]
        return epsilon, gamma

    def rate_oxygen_generator(self) -> int:
        filtered_lines = self.report_lines
        rank = 0

        while len(filtered_lines) > 1:
            filtered_lines = filter_by_most_common_value_at_rank(filtered_lines, rank)
            rank += 1

        final_value = filtered_lines[0]

        return int(final_value, 2)

    def rate_carbon_dioxyde_scrubber(self) -> int:
        filtered_lines = self.report_lines
        rank = 0

        while len(filtered_lines) > 1:
            filtered_lines = filter_by_least_common_value_at_rank(filtered_lines, rank)
            rank += 1

        final_value = filtered_lines[0]

        return int(final_value, 2)

    def consumption(self) -> int:
        return self.gamma_rate * self.epsilon_rate

    def rate_life_support(self) -> int:
        return self.rate_oxygen_generator() * self.rate_carbon_dioxyde_scrubber()


class Day03(Exercise):
    def part_one(self) -> int:
        report = DiagnosticReport(list(self.input_data))
        print(f"Gamma rate: \t{report.gamma_rate} \t({bin(report.gamma_rate)})")
        print(f"Epsilon rate: \t{report.epsilon_rate} \t({bin(report.epsilon_rate)})")
        consumption = report.consumption()
        print(f'Consumption: \t{consumption}')
        return consumption

    def part_two(self) -> int:
        report = DiagnosticReport(list(self.input_data))
        oxygen_generator = report.rate_oxygen_generator()
        print(f"O2 Generator rating {oxygen_generator} ({bin(oxygen_generator)})")
        carbon_dioxyde_scrubber = report.rate_carbon_dioxyde_scrubber()
        print(f"CO2 Generator rating {carbon_dioxyde_scrubber} ({bin(carbon_dioxyde_scrubber)})")
        life_support_rating = report.rate_life_support()
        print(f"Life support rating {life_support_rating}")
        return life_support_rating


if __name__ == '__main__':
    inputfile_path = get_input_data_filepath(__file__)
    with open(inputfile_path) as input_file:
        exercise = Day03(input_file.readlines())
        exercise.solve_all()
