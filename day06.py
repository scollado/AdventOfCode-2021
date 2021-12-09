from collections.abc import Sized

from aocutils.aoc import Exercise
from aocutils.file import get_input_data_filepath


class LanterFishGeneration(Sized):

    def __len__(self) -> int:
        return sum(self._current_generation)

    def __init__(self, starting_generation: str) -> None:
        super().__init__()
        initial_state = [int(fish) for fish in starting_generation.strip().split(',')]
        self._current_generation = [initial_state.count(age) for age in range(9)
                                    ]
        print(f'Initial state: {self}')

    def _decay(self):
        reseted_or_new_fishes = self._current_generation.pop(0)
        self._current_generation[6] += reseted_or_new_fishes
        self._current_generation.append(reseted_or_new_fishes)

    def pass_days(self, day_count: int):
        for day in range(day_count):
            self._decay()
            print(f'After day {str(day)}: {self._current_generation}')

    def __repr__(self) -> str:
        return str({age: count for age, count in enumerate(self._current_generation)})


class Day06(Exercise):

    def part_one(self) -> int:
        generation = LanterFishGeneration(list(self.input_data)[0])
        generation.pass_days(80)
        return len(generation)

    def part_two(self) -> int:
        generation = LanterFishGeneration(list(self.input_data)[0])
        generation.pass_days(256)
        return len(generation)


if __name__ == '__main__':
    inputfile_path = get_input_data_filepath(__file__)
    with open(inputfile_path) as input_file:
        exercise = Day06(input_file.readlines())
        exercise.solve_all()
