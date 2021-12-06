from typing import Optional, Iterable

from aocutils.aoc import Exercise
from aocutils.file import read_integer_file, get_input_data_filepath


def get_increment_value(current: int, previous: Optional[int] = None) -> int:
    if previous is None:
        print(f"❌ {current} — No previous value")
        return 0

    if current > previous:
        print(f"↗️ {current} — INCREASED")
        return 1
    elif current < previous:
        print(f"↘️ {current} — decreased")
    else:
        print(f"= {current} — no change")

    return 0


class SonarReport:

    def __init__(self, sweep_values: Iterable[int]) -> None:
        super().__init__()
        self.sweep_values = sweep_values

    def get_increases(self) -> int:
        increase_count = 0
        last_value: Optional[int] = None

        for current_value in self.sweep_values:
            increase_count += get_increment_value(current_value, last_value)
            last_value = current_value

        return increase_count


class SmoothedSonarReport(SonarReport):

    def __init__(self, sweep_values: list[int]) -> None:
        smoothed_sweep_values = [
            sum(sweep_values[window_start:(window_start + 3)]) for window_start in range(len(sweep_values) - 2)
        ]
        super().__init__(smoothed_sweep_values)


class Day01(Exercise):

    def __init__(self, input_data: list[int]) -> None:
        super().__init__(input_data)
        self.input_data = input_data

    def part_one(self) -> int:
        return SonarReport(self.input_data).get_increases()

    def part_two(self) -> int:
        return SmoothedSonarReport(self.input_data).get_increases()


if __name__ == '__main__':
    input_values = list(read_integer_file(get_input_data_filepath(__file__)))
    exercise = Day01(input_values)
    exercise.solve_all()
